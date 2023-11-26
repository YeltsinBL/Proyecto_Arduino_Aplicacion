"""Conexión a la BD SQL"""

#import pymssql
import pyodbc

def connectionBD():
    """Conexión a SQL Server"""
    try:
        # Conexión Remota SQL Server - pymssql
        # database = pymssql.connect(
        #     server="localhost:1433",
        #     user='SA',
        #     password='chemoSql123',
        #     database='Invernadero',
        #     as_dict=True)
        # if database:
        #     # print("Conexión exitosa a la BD")
        #     return database

        # Conexión Remota SQL Server - pyodbc
        SERVER = 'localhost'
        DATABASE = 'Invernadero'
        USERNAME = 'SA'
        PASSWORD = 'chemoSql123$'
        port= '1433'

        conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+SERVER+
                            ';PORT='+port+
                            ';DATABASE='+DATABASE+
                            ';UID='+USERNAME+
                            ';PWD='+ PASSWORD+
                            ';TrustServerCertificate=YES;'
                            )
        # cursor = conn.cursor()
        # cursor.execute(""" SELECT TABLE_NAME
        #      FROM INFORMATION_SCHEMA.TABLES
        #      WHERE TABLE_TYPE = 'BASE TABLE' """)
        # print(cursor.fetchall())
        return conn
    except Exception as error:
        print(f"No se pudo conectar: {error}")
