"""Redireccionar por algún error"""
from app import app
from flask import request, session, redirect, url_for


@app.errorhandler(404)
def page_not_found(error):
    """Redireccionar al inicio cuando hay errores"""
    if 'conectado' in session and request.method == 'GET':
        return redirect(url_for('inicio'))
    return redirect(url_for('inicio'))
