"""Rutas para los formularios desde el login"""

from app import app
from flask import render_template, request, flash, redirect, url_for, session

# Importando mi conexión a BD
from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importando controllers para el modulo de login
from controllers.funciones_login import *
PATH_URL_LOGIN = "public/login"

# Formulario login o dashboard
@app.route('/', methods=['GET'])
def inicio():
    """Formulario login o dashboard"""
    if 'conectado' in session:
        render_template('public/base_cpanel.html', dataLogin=data_login_sesion())
        return render_template('public/dahboard/dashboard.html', sectore = sql_lista_sectores())
    return render_template(f'{PATH_URL_LOGIN}/base_login.html')

# Formulario Perfil
@app.route('/mi-perfil', methods=['GET'])
def perfil():
    """Formulario de Perfil"""
    if 'conectado' in session:
        return render_template('public/perfil/perfil.html',
                               info_perfil_session=info_perfil_session())
    return redirect(url_for('inicio'))

# Registrar Usuario
@app.route('/register-user', methods=['GET'])
def cpanelRegisterUser():
    """Formulario Crear Cuenta"""
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    return render_template(f'{PATH_URL_LOGIN}/auth_register.html')

# Recuperar Contraseña
@app.route('/recovery-password', methods=['GET'])
def cpanelRecoveryPassUser():
    """Recuperar cuenta de usuario"""
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    return render_template(f'{PATH_URL_LOGIN}/auth_forgot_password.html')


# Crear cuenta de usuario
@app.route('/saved-register', methods=['POST'])
def cpanelResgisterUserBD():
    """Guardar cuenta y redireccionar al dashboard"""
    if request.method == 'POST' and 'name_surname' in request.form and 'pass_user' in request.form:
        name_surname = request.form['name_surname']
        email_user = request.form['email_user']
        pass_user = request.form['pass_user']
        resultado = recibeInsertRegisterUser( name_surname, email_user, pass_user)
        if resultado != 0:
            flash('la cuenta fue creada correctamente.', 'success')
            return redirect(url_for('inicio'))
        return redirect(url_for('inicio'))
    flash('el método HTTP es incorrecto', 'error')
    return redirect(url_for('inicio'))

# Actualizar datos del usuario
@app.route("/actualizar-datos-perfil", methods=['POST'])
def actualizarPerfil():
    """Actualizar datos del usuario"""
    if request.method == 'POST':
        if 'conectado' in session:
            respuesta = procesar_update_perfil(request.form)
            if respuesta == 1:
                flash('Los datos fuerón actualizados correctamente.', 'success')
                return redirect(url_for('inicio'))
            if respuesta == 0:
                flash(
                    'La contraseña actual esta incorrecta, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            if respuesta == 2:
                flash('Ambas claves deben se igual, por favor verifique.', 'error')
                return redirect(url_for('perfil'))
            if respuesta == 3:
                flash('La Clave actual es obligatoria.', 'error')
                return redirect(url_for('perfil'))
        else:
            flash('primero debes iniciar sesión.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

# Validar sesión
@app.route('/login', methods=['GET', 'POST'])
def loginCliente():
    """Mostrar formulario Login o Dashboard"""
    if 'conectado' in session:
        return redirect(url_for('inicio'))
    if request.method == 'POST' and 'email_user' in request.form and 'pass_user' in request.form:
        email_user = str(request.form['email_user'])
        pass_user = str(request.form['pass_user'])
        # Comprobando si existe una cuenta
        conexion_sql = connectionBD()
        cursor = conexion_sql.cursor()
        cursor.execute(
            """SELECT * FROM usuarios WHERE email_user = %s""", (email_user))
        account = cursor.fetchone()
        if account:
            if check_password_hash(account['pass_user'], pass_user):
                # Crear datos de sesión, para poder acceder a estos datos en otras rutas
                session['conectado'] = True
                session['id'] = account['id']
                session['name_surname'] = account['name_surname']
                session['email_user'] = account['email_user']
                flash('la sesión fue correcta.', 'success')
                return redirect(url_for('inicio'))
            # La cuenta no existe o el nombre de usuario/contraseña es incorrecto
            flash('datos incorrectos por favor revise.', 'error')
            return render_template(f'{PATH_URL_LOGIN}/base_login.html')
        flash('el usuario no existe, por favor verifique.', 'error')
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')
    flash('primero debes iniciar sesión.', 'error')
    return render_template(f'{PATH_URL_LOGIN}/base_login.html')

# Cerrar Sesión
@app.route('/closed-session',  methods=['GET'])
def cerraSesion():
    """Cerrar Sesión"""
    if request.method == 'GET':
        if 'conectado' in session:
            # Eliminar datos de sesión, esto cerrará la sesión del usuario
            session.pop('conectado', None)
            session.pop('id', None)
            session.pop('name_surname', None)
            session.pop('email', None)
            flash('tu sesión fue cerrada correctamente.', 'success')
            return redirect(url_for('inicio'))
        flash('recuerde debe iniciar sesión.', 'error')
        return render_template(f'{PATH_URL_LOGIN}/base_login.html')
