import pandas as pd
import mysql.connector

# Conectar a la base de datos MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='nnsae98n',  # No olvides insertar tu contraseña aquí
    database='bifsa',
    port=3306
)
cursor = connection.cursor()

# Ejecutar la consulta para obtener los kits
kits_query = """
SELECT p.cve_prod, p.desc_prod FROM products p
RIGHT JOIN bifsa.kit k ON p.cve_prod=k.cve_kit WHERE p.cse_prod NOT LIKE '%obsole%' GROUP BY k.cve_kit
"""
cursor.execute(kits_query)
kits_result = cursor.fetchall()

# Ejecutar la consulta para obtener los productos que pertenecen a cada kit
products_query = """
SELECT k.cve_kit, p.cve_prod, p.desc_prod, k.cantidad FROM products p
RIGHT JOIN bifsa.kit k ON p.cve_prod=k.cve_prod WHERE p.cse_prod NOT LIKE '%obsole%'
"""
cursor.execute(products_query)
products_result = cursor.fetchall()

# Crear DataFrames de pandas con los datos de kits y productos
kits_columns = ['ID Producto', 'Producto/Lista de materiales']
products_columns = ['ID Kit', 'ID Producto', 'Producto/Lista de materiales', 'Cantidad']

kits_df = pd.DataFrame(kits_result, columns=kits_columns)
products_df = pd.DataFrame(products_result, columns=products_columns)

# Combinar los DataFrames de kits y productos
combined_dfs = []
for _, kit_row in kits_df.iterrows():
    kit_row_df = pd.DataFrame(
        [[kit_row['ID Producto'], None, kit_row['Producto/Lista de materiales'], 1, 'Unidades', None, 'Kit', None,
          None, 'Unidades']],
        columns=['ID Producto', 'ID Kit', 'Producto/Lista de materiales', 'Cantidad', 'Unidad de medida', 'Empresa',
                 'Tipo de LdM', 'Líneas de LdM/Componente', 'Líneas de LdM/Cantidad',
                 'Líneas de LdM/Unidad de medida del producto']
    )
    products_in_kit = products_df[products_df['ID Kit'] == kit_row['ID Producto']].copy()
    products_in_kit['Unidad de medida'] = None
    products_in_kit['Empresa'] = None
    products_in_kit['Tipo de LdM'] = None
    products_in_kit['Líneas de LdM/Componente'] = products_in_kit['Producto/Lista de materiales']
    products_in_kit['Producto/Lista de materiales'] = None
    products_in_kit['Líneas de LdM/Cantidad'] = products_in_kit['Cantidad']
    products_in_kit['Cantidad'] = None
    products_in_kit['Líneas de LdM/Unidad de medida del producto'] = 'Unidades'
    products_in_kit = products_in_kit[
        ['ID Producto', 'ID Kit', 'Producto/Lista de materiales', 'Cantidad', 'Unidad de medida', 'Empresa',
         'Tipo de LdM', 'Líneas de LdM/Componente', 'Líneas de LdM/Cantidad',
         'Líneas de LdM/Unidad de medida del producto']]

    combined_dfs.append(kit_row_df)
    combined_dfs.append(products_in_kit)

combined_df = pd.concat(combined_dfs, ignore_index=True)

# Guardar el DataFrame en un archivo de Excel
output_file = 'Kits_Formato_Excel.xlsx'
combined_df.to_excel(output_file, index=False, engine='openpyxl')

# Cerrar la conexión
cursor.close()
connection.close()
