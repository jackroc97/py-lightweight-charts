import threading

from dataclasses import dataclass
from enum import Enum
from flask import Flask, render_template
from flask_socketio import SocketIO


@dataclass
class Marker:
    time: int
    position: str
    color: str
    shape: str
    text: str
    
    
    def to_dict(self) -> dict:
        return {
            'time': self.time,
            'position': self.position,
            'color': self.color,
            'shape': self.shape,
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
    
        
    def set_markers(self, markers: list[Marker]) -> None:
        """
        Set markers on the series.

        Args:
            markers (list[Marker]): A list of markers to be added to the series.
        """
        self.socketio.emit('set_markers', (self.id, 
                                           [m.to_dict() for m in markers]))
        
        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'type': self.type.name.lower(),
            'options': self.options | {}
        }
        

class Chart:
    """
    Represents a single lightweightcharts Chart object.  Charts are added to the
    app using `PyLightweightCharts.add_chart(...)`.
    """
    
    def __init__(self, id: str, options: dict = {}):
        self.id = id
        self.options = options
        self.socketio: SocketIO = None
        

    def update_series(self, series: Series, data: dict) -> None:
        """
        Update a series of data on this chart.  The method is smart such that if
        the series does not yet exist on the chart, it will be automatically
        added to the chart.

        Args:
            series (Series): The series to be added or updated.
            data (dict): The last data point to update the chart with.
        """
        series.socketio = self.socketio
        self.socketio.emit('update_series', (self.to_dict(), 
                                             series.to_dict(), 
                                             data))
        
        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'options': self.options | {}
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
    
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.thread = None
        
        # Define routes
        @self.app.route('/')
        def home():
            return render_template('index.html')
        
    
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
        
        kwargs = {'host': host, 'port': port, 'allow_unsafe_werkzeug': True}
        self.thread = threading.Thread(target=self.socketio.run, 
                                       args=(self.app, ), 
                                       kwargs=kwargs)
        self.thread.daemon = daemon
        self.thread.start()
                
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
