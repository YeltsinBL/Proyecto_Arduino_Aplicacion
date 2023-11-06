from app import app, socketio
from flask import render_template, request, flash, redirect, url_for, session,  jsonify

# Importando conexión a BD
from controllers.funciones_home import *
import serial
PATH_URL = "public/mediciones"

# region Medición
@app.route('/registrar-medicion', methods=['GET'])
def view_form_medicion():
    """Mostrar el formulario de medición"""
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_medicion.html')
    flash('primero debes iniciar sesión.', 'error')
    return redirect(url_for('inicio'))

@app.route('/form-registrar-medicion', methods=['POST'])
def form_medicion():
    """Registar una medición"""
    if 'conectado' in session:
        print(request.form)
        resultado = procesar_form_medicion(request.form)
        if resultado:
            socketio.emit('datosmedicion', emitir_socket(request.form))
            # llamamos a esta función para que muestre el formulario
            return redirect(url_for('lista_mediciones'))
        flash('La medición NO fue registrado.', 'error')
        return render_template(f'{PATH_URL}/form_medicion.html')
    flash('primero debes iniciar sesión.', 'error')
    return redirect(url_for('inicio'))

@app.route('/lista-de-mediciones', methods=['GET'])
def lista_mediciones():
    """Mostrar el formulario de listado de mediciones"""
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_medicion.html',
                               mediciones=sql_lista_medicion())
    flash('primero debes iniciar sesión.', 'error')
    return redirect(url_for('inicio'))

@app.route("/buscando-medicion", methods=['POST'])
def view_buscar_mediciones():
    """Buscar las mediciones en el formulario de listado"""
    resultado_busqueda = buscar_medicion_fechas(request.json['fecha_desde'],
                                                request.json['fecha_hasta'])
    if resultado_busqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_medicion.html',
                               dataBusqueda=resultado_busqueda)
    return jsonify({'fin': 0})
@app.route("/buscando-medicion-sector", methods=['POST'])
def view_buscar_mediciones_sector():
    """Buscar las mediciones por sector en el Dashboard"""
    resultado_busqueda = buscar_medicion_sector(request.json['valor'])
    if resultado_busqueda:
        return render_template('public/dahboard/graficos.html',
                               dataBusqueda=resultado_busqueda)
    return jsonify({'fin': 0})
@app.route("/buscando-medicion-sector-temperatura", methods=['POST'])
def view_buscar_mediciones_sector_temperatura():
    """Buscar las mediciones por sector en el Dashboard"""
    resultado_busqueda = buscar_medicion_sector(request.json['valor'],False)
    if resultado_busqueda:
        return render_template('public/dahboard/grafico_temperatura.html',
                               dataBusqueda=resultado_busqueda)
    return jsonify({'fin': 0})
@app.route("/descargar-informe-mediciones/", methods=['GET'])
def reporte_medicion():
    """Generar el reporte en excel de mediciones"""
    if 'conectado' in session:
        return generar_reporte_excel_medicion()
    flash('primero debes iniciar sesión.', 'error')
    return redirect(url_for('inicio'))

@app.route("/lista_puertos_disponibles", methods=['POST'])
def lista_puertos_disponibles():
    """Buscar las mediciones por sector en el Dashboard"""
    return jsonify(listar_puertos())

serialobj:serial
@socketio.event
def acciones_arduino(datos):
    """Establecer conexión con el arduino"""
    print(datos)
    valor_sensor=0
    global serialobj
    try:
        if datos['boton'] == 'conn':
            serialobj = serial.Serial(datos['valor'],9600)
            if serialobj.isOpen():
                serialobj.close()
            serialobj.open()
            print('com3 is open', serialobj.isOpen())
        if datos['boton'] == 'on':
            serialobj.write(str(datos['valor']).encode())
        if datos['boton'] == 'right':
            serialobj.write(str(datos['valor']).encode())
        if datos['boton'] == 'left':
            serialobj.write(str(datos['valor']).encode())
        if datos['boton'] == 'dis':
            serialobj.write(str(datos['valor']).encode())
            serialobj.close()
            print('com3 is open', serialobj.isOpen())
        if serialobj.isOpen() and (datos['boton'] in {'on','right','left'}):
            valor_sensor= int(serialobj.readline().decode('ascii'))
            print("valor_sensor: ",valor_sensor)
        datos['dato_sensor']=valor_sensor
        print(datos)
        socketio.emit('datosarduino', datos)
    except Exception:
        print('No se llegó los datos')
    return redirect(url_for('view_form_medicion'))

#endregion

#region Usuario


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    """Formulario Lista Usuario"""
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    """Eliminar Usuario"""
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))

#endregion
