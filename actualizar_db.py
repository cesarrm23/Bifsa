import pandas as pd
import mysql.connector

# Leer los datos desde el archivo Excel
file = 'precios.xlsx'
df = pd.read_excel(file, engine='openpyxl')

# Conectar a la base de datos MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='nnsae98n',  # No olvides insertar tu contraseña aquí
    database='bifsa',
    port=3306
)
cursor = connection.cursor()

# Actualizar los datos en la tabla 'products' por medio de la columna 'cve_prod'
for index, row in df.iterrows():
    update_query = f"""
        UPDATE products SET
            cto_ent = '{row['cto_ent']}',
            precc = '{row['precc']}'
        WHERE cve_prod = '{row['cve_prod']}'
    """
    cursor.execute(update_query)

# Confirmar y cerrar la conexión
connection.commit()
cursor.close()
connection.close()
