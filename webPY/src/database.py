"""Clase de Conexión a la BD"""
import pymssql
# Conexión Remota

database = pymssql.connect(
        server="localhost:1433",
        user='SA',
        password='chemoSql123',
        database='SesionToken',
        as_dict=True)
