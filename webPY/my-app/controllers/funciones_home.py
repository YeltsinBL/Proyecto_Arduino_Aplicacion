"""Funciones de Lógica para el Home"""

import datetime
import os
from conexion.conexionBD import connectionBD  # Conexión a BD

import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file

import serial.tools.list_ports as list_comports

#region Medición

def procesar_form_medicion(data_form):
    """Guardar Medición"""
    try:
        with connectionBD() as conexion_sql:
            with conexion_sql.cursor() as cursor:

                sql = "INSERT INTO mediciones (humedad_inicial, humedad_final, temperatura_inicial,\
                    temperatura_final, fecha_registro, sector_id)\
                    VALUES (%s, %s, %s, %s, %s, %s)"
                first = data_form['medicion_fecha'].replace(",", "")
                second =datetime.datetime.strptime(first, '%d/%m/%Y %H:%M:%S')
                # Creando una tupla con los valores del INSERT
                valores = (data_form['medicion_humedad_inicial'], data_form['medicion_humedad_final'],
                        data_form['medicion_temperatura_inicial'], data_form['medicion_temperatura_final'],
                        second, data_form['medicion_sector'])
                cursor.execute(sql, valores)
                conexion_sql.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert
    except Exception as e:
        return f'Se produjo un error en procesar_form_medicion: {str(e)}'

def sql_lista_medicion():
    """Listar Medición"""
    try:
        with connectionBD() as conexion_sql:
            with conexion_sql.cursor() as cursor:
                query = """
                    SELECT idmediciones, humedad_inicial, humedad_final, temperatura_inicial, temperatura_final,
                            FORMAT( fecha_registro, 'dd/MM/yyyy', 'en-US' ) +' '+
							FORMAT(fecha_registro, N'hh:mm tt') AS fecha_registro,
                        s.Sector_Nombre AS medicion_sector
                    FROM mediciones m 
					inner join Sector s on m.sector_id = s.idSector
                    ORDER BY m.fecha_registro desc
                    """
                cursor.execute(query)
                mediciones = cursor.fetchall()
        return mediciones
    except Exception as e:
        print(
            f"Errro en la función sql_lista_medicion: {e}")
        return None

def medicion_reporte():
    """Obtener datos para el Reporte en Excel de las mediciones"""
    try:
        with connectionBD() as conexion_sql:
            with conexion_sql.cursor() as cursor:
                query = """
                    SELECT humedad_inicial, humedad_final, temperatura_inicial, temperatura_final,
                        FORMAT( fecha_registro, 'dd/MM/yyyy', 'en-US' ) +' '+
						    FORMAT(fecha_registro, N'hh:mm tt') AS fecha_registro,
                        s.Sector_Nombre AS medicion_sector
                    FROM mediciones m 
					inner join Sector s on m.sector_id = s.idSector
                    ORDER BY m.fecha_registro desc
                    """
                cursor.execute(query)
                mediciones = cursor.fetchall()
        return mediciones
    except Exception as e:
        print(
            f"Error en la función medicion_reporte: {e}")
        return None

def generar_reporte_excel_medicion():
    """Reporte de Excel para Mediciones"""
    data_mediciones = medicion_reporte()
    wb = openpyxl.Workbook()
    hoja = wb.active

    # Agregar la fila de encabezado con los títulos
    cabecera_excel = ("Sector", "Fecha de Ingreso", "Humedad Inicial", "Humedad Final",
                     "Temperatura Inicial", "Temperatura Final")

    hoja.append(cabecera_excel)

    # Agregar los registros a la hoja
    for registro in data_mediciones:
        medicion_sector = registro['medicion_sector']
        fecha_registro = registro['fecha_registro']
        humedad_inicial = registro['humedad_inicial']
        humedad_final = registro['humedad_final']
        temperatura_inicial = registro['temperatura_inicial']
        temperatura_final = registro['temperatura_final']

        # Agregar los valores a la hoja
        hoja.append((medicion_sector, fecha_registro, humedad_inicial,
                    humedad_final, temperatura_inicial, temperatura_final))

    fecha_actual = datetime.datetime.now()
    archivo_excel = f"Reporte_Medicion_{fecha_actual.strftime('%Y_%m_%d')}.xlsx"
    # Guardar en la carpeta Downloads
    carpeta_descarga = os.path.expanduser("~")
    ruta_descarga = os.path.join(carpeta_descarga, "Downloads")

    ruta_archivo = os.path.join(ruta_descarga, archivo_excel)
    wb.save(ruta_archivo)

    # Enviar el archivo como respuesta HTTP
    return send_file(ruta_archivo, as_attachment=True)

def buscar_medicion_fechas(fecha_desde, fecha_hasta):
    """Buscar Medición por Fechas"""
    try:
        with connectionBD() as conexion_sql:
            with conexion_sql.cursor() as cursor:
                query = """
                    SELECT idmediciones, humedad_inicial, humedad_final, temperatura_inicial, temperatura_final,
                        FORMAT( fecha_registro, 'dd/MM/yyyy', 'en-US' ) +' '+
							FORMAT(fecha_registro, N'hh:mm tt') AS fecha_registro,
                        s.Sector_Nombre AS medicion_sector
                    FROM mediciones m 
					inner join Sector s on m.sector_id = s.idSector
                    WHERE (%s = '' and %s='') or 
                          (CAST(fecha_registro AS date) >= convert(date, %s, 103) and
                          CAST(fecha_registro AS date) <= convert(date, %s, 103))
                    ORDER BY m.fecha_registro desc;
                    """
                search_pattern =(fecha_desde, fecha_hasta,fecha_desde, fecha_hasta)
                cursor.execute(query, search_pattern)
                resultado_busqueda = cursor.fetchall()
                return resultado_busqueda
    except Exception as e:
        print(f"Ocurrió un error en def buscar_medicion_fechas: {e}")
        return []

def buscar_medicion_sector(valor, humedad=True):
    """Buscar Medición por Sector"""
    try:
        with connectionBD() as conexion_sql:
            with conexion_sql.cursor() as cursor:
                if humedad:
                    query = """
                    declare @numero integer;
					set @numero =0;
                    select ROW_NUMBER() OVER(ORDER BY idmediciones ASC) AS _row,numero,humedad_inicial,fecha_registro from (
                        (SELECT @numero+1 as numero,idmediciones, humedad_inicial,
                        FORMAT( fecha_registro, 'dd/MM/yyyy', 'en-US' ) +' '+
							FORMAT(fecha_registro, N'hh:mm tt') AS fecha_registro
                        FROM mediciones
                        WHERE sector_id=3) 
                        UNION ALL
                        (SELECT @numero+1 as numero,
                           idmediciones,  humedad_final,
                        FORMAT( fecha_registro, 'dd/MM/yyyy', 'en-US' ) +' '+
							FORMAT(fecha_registro, N'hh:mm tt') AS fecha_registro
                        FROM mediciones
                            WHERE sector_id=3) 
				    ) as consulta where humedad_inicial is not null
                    """
                else:
                    query ="""
                    declare @numero integer;
					set @numero =0;
                    select ROW_NUMBER() OVER(ORDER BY idmediciones ASC) AS _row,numero,temperatura_inicial,fecha_registro from (
	
                        (SELECT @numero+1 as numero,idmediciones, temperatura_inicial,
                            FORMAT( fecha_registro, 'dd/MM/yyyy', 'en-US' ) +' '+
							    FORMAT(fecha_registro, N'hh:mm tt') AS fecha_registro
                            FROM mediciones
                            WHERE sector_id=3) 
                        UNION ALL
                        (SELECT  @numero+2 as numero,idmediciones,  temperatura_final,
                            FORMAT( fecha_registro, 'dd/MM/yyyy', 'en-US' ) +' '+
							    FORMAT(fecha_registro, N'hh:mm tt') AS fecha_registro
                            FROM mediciones
                            WHERE sector_id=3)
				    ) as consulta where temperatura_inicial is not null
                    """
                cursor.execute(query, (valor,valor))
                resultado_busqueda = cursor.fetchall()
                print(resultado_busqueda)
                return resultado_busqueda
    except Exception as e:
        print(f"Ocurrió un error en def buscar_medicion_fechas: {e}")
        return []
#endregion

#region Sockets

def emitir_socket(data_form):
    """Formatear datos para el socket"""
    first = data_form['medicion_fecha'].replace(",", "")
    second =datetime.datetime.strptime(first, '%d/%m/%Y %H:%M:%S')
    nuevo_formato = second.strftime("%d/%m/%Y %I:%M %p")
    return {"fecha_registro":nuevo_formato,
           "humedad": data_form['medicion_humedad_inicial']+","+
                        data_form['medicion_humedad_final'],
           "temperatura": data_form['medicion_temperatura_inicial']+","+
                        data_form['medicion_temperatura_final'],
            "medicion_sector": data_form['medicion_sector']}

def listar_puertos():
    """Lista de los puertos disponibles"""
    # Listar los puertos disponibles
    list_ports = []
    get_ports = list_comports.comports()
    for port in sorted(get_ports):
        list_ports.append(port.name)
    return list_ports

#endregion

#region Usuario

def lista_usuariosBD():
    """Lista de Usuarios"""
    try:
        with connectionBD() as conexion_sql:
            with conexion_sql.cursor() as cursor:
                query_sql = "SELECT id, name_surname, email_user, created_user FROM usuarios"
                cursor.execute(query_sql)
                usuarios_list = cursor.fetchall()
        return usuarios_list
    except Exception as e:
        print(f"Error en lista_usuariosBD : {e}")
        return []

def eliminarUsuario(id):
    """Eliminar usuario"""
    try:
        with connectionBD() as conexion_sql:
            with conexion_sql.cursor() as cursor:
                query_sql = "DELETE FROM usuarios WHERE id=%s"
                cursor.execute(query_sql, (id,))
                conexion_sql.commit()
                resultado_eliminar = cursor.rowcount
        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarUsuario : {e}")
        return []

#endregion
