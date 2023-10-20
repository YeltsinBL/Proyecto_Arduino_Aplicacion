from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import os


from random import random
from threading import Lock
from datetime import datetime

"""Background Thread"""
thread = None
thread_lock = Lock()

# accedemos a la carpeta principal del proyecto
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# unimos la carpeta SRC a la principal
template_dir = os.path.join(template_dir, 'src','template')
app = Flask(__name__, template_folder=template_dir)
app.config["SECRET_KEY"]= 'secret'
socketio = SocketIO(app,  cors_allowed_origins='*') # empieza la conexión

@app.route('/')
def home():
    """Página principal"""
    return render_template('grafico.html')

def get_current_datetime():
    """ Get current date time """
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")


def background_thread():
    """
    Generate random sequence of dummy sensor values and send it to our clients
    """
    print("Generating random sensor values")
    while True:
        dummy_sensor_value = round(random() * 100, 3)
        socketio.emit('updateSensorData', {'value': dummy_sensor_value,
                                           "date": get_current_datetime()})
        socketio.sleep(1)


@socketio.on('connect')
def connect():
    """ Decorator for connect """
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect')
def disconnect():
    """ Decorator for disconnect """
    print('Client disconnected',  request.sid)


if __name__ == '__main__':
    socketio.run(app)
