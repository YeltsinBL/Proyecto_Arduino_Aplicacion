"""Conexión a la BD SQL"""

import pymssql

def connectionBD():
    """Conexión a SQL Server"""
    try:
        # Conexión Remota SQL Server
        database = pymssql.connect(
            server="localhost:1433",
            user='SA',
            password='chemoSql123',
            database='Invernadero',
            as_dict=True)
        if database:
            print("Conexión exitosa a la BD")
            return database
    except Exception as error:
        print(f"No se pudo conectar: {error}")
