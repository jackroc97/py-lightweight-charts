import threading
import webbrowser

from dataclasses import dataclass
from enum import Enum
from flask import Flask, render_template
from flask_socketio import SocketIO
from re import sub


def camel_case(s: str) -> str:
    """
    Convert a string to camel case (e.g., "Camel Case" -> "camelCase").

    Args:
        s (str): String to convert to camel case.

    Returns:
        str: The string in camel case.
    """
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])


class SeriesMarkerPosition(Enum):
    ABOVE_BAR = 1,
    BELOW_BAR = 2,
    IN_BAR = 3,
    

class SeriesMarkerShape(Enum):
    CIRCLE = 1,
    SQUARE = 2,
    ARROW_UP = 3,
    ARROW_DOWN = 4,


@dataclass
class SeriesMarker:
    """
    Represents a marker, such as an arrow or circle, on a series of data.
    """
    time: int
    position: SeriesMarkerPosition
    shape: SeriesMarkerShape
    color: str
    text: str
    
    
    def to_dict(self) -> dict:
        return {
            'time': self.time,
            'position': camel_case(self.position.name),
            'shape': camel_case(self.shape.name),
            'color': self.color,
            'text': self.text
        }
    

class SeriesType(Enum):
    AREA = 1,
    BAR = 2,
    BASELINE = 3,
    CANDLESTICK = 4,
    HISTOGRAM = 5,
    LINE = 6,
    

@dataclass
class Series:
    """
    Represents a series of data to be displayed on the chart.
    """
    id: str
    type: SeriesType
    options: dict = None
    socketio: SocketIO = None
     
     
    def set_data(self, data: list[dict]) -> None:
        """
        Set the data for the series.

        Args:
            data (list[dict]): A list of dictionaries representing the data to be
                displayed on the chart.
        """
        if self.socketio is None:
            raise Exception("Series must be added to a chart before setting data.")
        
        self.socketio.emit('set_data', (self.id, data))
        
        
    def update(self, data: dict) -> None:
        """
        Update the series with new data.

        Args:
            data (dict): The last data point to update the series with.
        """
        if self.socketio is None:
            raise Exception("Series must be added to a chart before updating data.")
        
        self.socketio.emit('update', (self.id, data))
    
    
    def set_markers(self, markers: list[SeriesMarker]) -> None:
        """
        Set markers on the series.

        Args:
            markers (list[Marker]): A list of markers to be added to the series.
        """
        if self.socketio is None:
            raise Exception("Series must be added to a chart before setting markers.")
        
        self.socketio.emit('set_markers', (self.id, 
                                           [m.to_dict() for m in markers]))
        
        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'type': self.type.name.lower(),
            'options': self.options or {}
        }
        

@dataclass
class Chart:
    """
    Represents a single lightweightcharts Chart object.  Charts are added to the
    app using `PyLightweightCharts.add_chart(...)`.
    """
    id: str
    options: dict = None
    socketio: SocketIO = None
        

    def add_series(self, series: Series, pane_id: int=0) -> None:
        """
        Add a series of data to the chart.

        Args:
            series (Series): The series to be added to the chart.
        """
        series.socketio = self.socketio
        self.socketio.emit('add_series', (self.to_dict(), 
                                          series.to_dict(), 
                                          pane_id))

        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'options': self.options or {}
        }


class PyLightweightCharts:
    """
    This object is the manager for the charts application.  It creates a Flask
    webserver that hosts a small front end application that this library talks
    to via websockets. 
    
    Example usage:
    ```python
    plwc = PyLightweightCharts()
    plwc.start()
    
    # Create and update charts here
    ...
    
    plwc.stop()
    ```
    """
    
    def __init__(self, chart_name: str):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.thread = None
        
        # Define routes
        @self.app.route('/')
        def home():
            return render_template('index.html', title=chart_name)
        
    
    def add_chart(self, chart: Chart) -> None:
        """
        Add a new chart to the page.

        Args:
            chart (Chart): The chart to be added to the page
        """
        
        chart.socketio = self.socketio
        
        # Block until we receive a response from the client
        # Once the client send the response, we know that the chart has been
        # added and it is safe to access it
        ev = threading.Event()
        def blocker():
            nonlocal ev
            ev.set()
        
        self.socketio.emit('add_chart', chart.to_dict(), callback=blocker)
        ev.wait()
        
        
    def start(self, host: str = '0.0.0.0', port: int = 5000, 
              daemon: bool = True) -> None:
        """
        Starts the webserver that host the chart application.

        Args:
            host (str, optional): Host IP. Defaults to '0.0.0.0'.
            port (int, optional): Port on the host. Defaults to 5000.
            daemon (bool, optional): Whether or not to run the chart in daemon
                thread.  Use `daemon = False` for displaying staic data.
                Defaults to True.
        """
        
        self.host = host
        self.port = port
        
        kwargs = {'host': host, 'port': port, 'allow_unsafe_werkzeug': True}
        self.thread = threading.Thread(target=self.socketio.run, 
                                       args=(self.app, ), 
                                       kwargs=kwargs)
        self.thread.daemon = daemon
        self.thread.start()
        
        threading.Timer(1, self._open_browser).start()
                
        # Wait for the client to send a "ready" socket message
        # This will block until the client-side script is running 
        # and is ready to accept messages from the server, such as adding
        # charts and updating data series
        ev = threading.Event()
        @self.socketio.on('ready')
        def ready():
            nonlocal ev
            ev.set()            
        ev.wait()
   
            
    def stop(self) -> None:  
        """
        Stop the server.
        """
        self.thread.join()
        
    
    def _open_browser(self):
      webbrowser.open_new(f"http://127.0.0.1:{self.port}")
