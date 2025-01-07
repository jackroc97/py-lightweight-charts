from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
from enum import Enum


# class SeriesType(Enum):
#     AREA = 'area',
#     BAR = 'bar',
#     BASELINE = 'baseline',
#     CANDLESTICK = 'candlestick',
#     HISTOGRAM = 'histogram',
#     LINE = 'line',
    

# class Series:
    
#     def __init__(self, id: str, type: SeriesType, options: dict = {}):
#         self.id = id
#         self.type = type
#         self.options = options
#         self.data = 
        
    
        

class Chart:
    
    def __init__(self, id: str, options: dict = {}):
        self.id = id
        self.options = options
        self.socketio: SocketIO = None
        

    def update_data(self, data):
        self.socketio.emit('update_series', (self.to_dict(), data))
        
        
    def to_dict(self):
        return {
            'id': self.id,
            'options': self.options
        }


class PyLightweightCharts:
    
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.thread = None
        
        # Define routes
        @self.app.route('/')
        def home():
            return render_template('index.html')
        
    
    def add_chart(self, chart: Chart):
        chart.socketio = self.socketio
        self.socketio.emit('add_chart', chart.to_dict())
        

    def start(self, host: str = '0.0.0.0', port: int = 5000):
        kwargs = {'host': host, 'port': port, 'allow_unsafe_werkzeug': True}
        self.thread = threading.Thread(target=self.socketio.run, 
                                       args=(self.app, ), 
                                       kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()
        

    def stop(self): 
        self.thread.join()

        


