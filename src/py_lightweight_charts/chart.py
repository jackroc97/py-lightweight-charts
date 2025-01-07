from flask import Flask, render_template
from flask_socketio import SocketIO
import threading


class Chart:
    
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.thread = None
        
        # Define routes
        @self.app.route('/')
        def home():
            return render_template('index.html')


    def update_data(self, data):
        self.socketio.emit('update', data)


    def start(self, host: str = '0.0.0.0', port: int = 5000):
        kwargs = {'host': host, 'port': port, 'allow_unsafe_werkzeug': True}
        self.thread = threading.Thread(target=self.socketio.run, 
                                       args=(self.app, ), 
                                       kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()
        

    def stop(self): 
        self.thread.join()
