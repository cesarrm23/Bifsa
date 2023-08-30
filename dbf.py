import pyodbc

# Ruta al archivo DBF
dbf_file = 'I:/01 bifsa/DB/EMP21/pedidoc.DBF'

# Cadena de conexión ODBC
connection_string = f"Driver={{Microsoft Visual FoxPro Driver}};SourceType=DBF;SourceDB={dbf_file};"

# Establecer la conexión
conn = pyodbc.connect(connection_string)

# Obtener el cursor
cursor = conn.cursor()

# Obtener la lista de columnas de la tabla
tabla = 'comprac'
consulta = f"SELECT * FROM {tabla} WHERE 1=0"
cursor.execute(consulta)

# Obtener los nombres de las columnas
nombres_columnas = [column[0] for column in cursor.description]

# Cerrar la conexión
conn.close()

# Imprimir los nombres de las columnas
for columna in nombres_columnas:
    print(columna)


import pandas as pd
import pyodbc
from openpyxl.workbook import Workbook

# Ruta al archivo DBF
dbf_file = 'I:/01 bifsa/DB/EMP21/comprac.DBF'

# Cadena de conexión ODBC
connection_string = f"Driver={{Microsoft Visual FoxPro Driver}};SourceType=DBF;SourceDB={dbf_file};"

# Establecer la conexión
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()
consulta = "SELECT * FROM pedidoc"
cursor.execute(consulta)
# Obtener los nombres de las columnas del cursor
columnas = [column[0] for column in cursor.description]

# Obtener los datos de las filas del cursor
datos = cursor.fetchall()
conn.close()
# Crear un DataFrame de Pandas
df = pd.DataFrame(datos, columns=columnas)
# Crear un libro de trabajo de Excel
libro_excel = Workbook()

# Seleccionar la hoja activa
hoja_activa = libro_excel.active

# Escribir los datos del DataFrame en la hoja activa
for indice, fila in df.iterrows():
    for columna, valor in enumerate(fila):
        hoja_activa.cell(row=indice+1, column=columna+1, value=valor)

# Guardar el archivo de Excel
archivo_excel = '/results/bajop2.xlsx'
libro_excel.save(archivo_excel)

