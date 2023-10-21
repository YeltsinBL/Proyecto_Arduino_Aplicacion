"""Aplicación de Python Principal"""
import os
from threading import Lock
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import database as db

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
    """Página principal HTML"""
    return render_template('grafico.html')

def background_thread():
    """ Obtener valores para el Gráfico al mostrar la página"""
    SQL_QUERY = """
    select CONCAT(CONVERT(varchar(50),Temperatura_Inicial_Fecha,103),' ',CONVERT(varchar(50),
    Temperatura_Inicial_Fecha,24)) as [Fecha Temperatura Inicial],
	CONVERT(varchar(6),Temperatura_Inicial) as [Temperatura Inicial] from Estadistica
    """
    cursor = db.database.cursor()
    cursor.execute(SQL_QUERY)
    records = cursor.fetchall()
    cursor.close()
    for record in records:
        emit('updateSensorData', {'value': record.get("Temperatura Inicial"),
                                    "date": record.get("Fecha Temperatura Inicial")})
        socketio.sleep(1)


@socketio.on('connect')
def connect():
    """Principal - Decorator for connect """
    background_thread()
    print('Client connected')
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(background_thread)
@socketio.event
def my_room_event(message):
    """Registrar en BD y obtener el valor de registro para agregarlo al Socket"""
    if message['descripcion'] and message['temperatura_inicial'] and\
        message['temperatura_final'] and message['humedad_inicial'] and message['humedad_final'] :
        cursor=db.database.cursor()
        sql = "insert into Estadistica (Descripcion, Temperatura_Inicial, Temperatura_Final,\
            Humedad_Inicial, Humedad_Final) values(%s,%s,%s,%s,%s);"
        data = (message['descripcion'], message['temperatura_inicial'],
                message['temperatura_final'], message['humedad_inicial'],
                message['humedad_final'])
        cursor.execute(sql,data)
        db.database.commit()
        id_inserted = cursor.lastrowid
        print("Id Registrado", id_inserted)
        cursor.close()
        print("Obteniendo información")
        cursor = db.database.cursor()
        sql="select CONCAT(CONVERT(varchar(50),Temperatura_Inicial_Fecha,103),' ',\
            CONVERT(varchar(50), Temperatura_Inicial_Fecha,24)) as [Fecha Temperatura Inicial],\
            CONVERT(varchar(6),Temperatura_Inicial) as [Temperatura Inicial] from Estadistica\
            where IdEStadistica=%s"
        cursor.execute(sql, id_inserted)
        records = cursor.fetchall()
        cursor.close()
        for record in records:
            emit('updateSensorData', {'value': record.get("Temperatura Inicial"),
                                    "date": record.get("Fecha Temperatura Inicial")},
                                    broadcast=True)

@socketio.on('disconnect')
def disconnect():
    """ Decorator for disconnect """
    print('Client disconnected',  request.sid)


if __name__ == '__main__':
    socketio.run(app)
