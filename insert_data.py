import pandas as pd
import mysql.connector

# Leer los datos desde el archivo Excel
file = 'resultado.xlsx'
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

# Insertar los datos en la tabla 'new_table'
for index, row in df.iterrows():
    insert_query = f"""
        INSERT INTO new_table (
            cse_prod, cve_prod, desc_prod, uni_med, sub_cse, sub_subcse,
            concat_clas, sku, nva_desc, valores
        ) VALUES (
            '{row['cse_prod']}', '{row['cve_prod']}', '{row['desc_prod']}', '{row['uni_med']}',
            '{row['sub_cse']}', '{row['sub_subcse']}', '{row['concat_clas']}', '{row['sku']}',
            '{row['nva_desc']}', '{row['valores']}'
        )
    """
    cursor.execute(insert_query)

# Confirmar y cerrar la conexión
connection.commit()
cursor.close()
connection.close()




import pandas as pd
import mysql.connector

# Leer los datos desde el archivo Excel
file = 'Cata_prd_20230414_001UX7.xlsx'
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

# Insertar los datos en la tabla 'new_table'
for index, row in df.iterrows():
    insert_query = f"""
        INSERT INTO products (
            cse_prod, cve_prod, desc_prod, uni_med, cto_ent, staiva,
            cve_tial, cto_ant, cve_monp, cve_monc, cve_mona, desc_prod2, conv_var, 
            staretiva, kit, sub_cse, sub_subcse, trans,
            staretisr, c_prds, staimpto1, staimpto2, des1, des2
        ) VALUES (
            '{row['cse_prod']}', '{row['cve_prod']}', '{row['desc_prod']}', '{row['uni_med']}',
            '{row['cto_ent']}', '{row['staiva']}', '{row['cve_tial']}', '{row['cto_ant']}',
            '{row['cve_monp']}', '{row['cve_monc']}', '{row['cve_mona']}', '{row['desc_prod2']}', '{row['conv_var']}',
             '{row['staretiva']}', '{row['kit']}', '{row['sub_cse']}', '{row['sub_subcse']}', '{row['trans']}', 
             '{row['staretisr']}', '{row['c_prds']}', '{row['staimpto1']}', '{row['staimpto2']}',
             '{row['des1']}', '{row['des2']}'
        )
    """
    cursor.execute(insert_query)

# Confirmar y cerrar la conexión
connection.commit()
cursor.close()
connection.close()