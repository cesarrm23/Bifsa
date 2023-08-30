import pymysql
import pandas as pd

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="nnsae98n",
    db="bifsa"
)

# Consulta SQL
sql_query = """
SELECT 
    TRIM(TRAILING ',' FROM REPLACE((CASE WHEN COUNT(pv.cve_prod) > 1 
        THEN GROUP_CONCAT(TRIM(pv.cve_prod), ',') 
        ELSE GROUP_CONCAT(TRIM(pv.cve_prod)) 
    END), ',,', ',')) AS claves,
    pv.nva_desc,
    TRIM(TRAILING ',' FROM REPLACE((CASE WHEN COUNT(pv.valores) > 1 
        THEN GROUP_CONCAT(TRIM(REPLACE(pv.valores,',',' ')), ',') 
        ELSE GROUP_CONCAT(TRIM(REPLACE(pv.valores,',',' '))) 
    END), ',,', ',')) AS valores,
    TRIM(TRAILING ',' FROM REPLACE((CASE WHEN COUNT(p.cto_ent) > 1 
        THEN GROUP_CONCAT(TRIM(p.cto_ent), ',') 
        ELSE GROUP_CONCAT(TRIM(p.cto_ent)) 
    END), ',,', ',')) AS costos
FROM 
    bifsa.new_table pv
LEFT JOIN bifsa.products p ON pv.cve_prod=p.cve_prod
WHERE
    pv.valores != 'nan' AND p.kit = 0
GROUP BY 
    pv.nva_desc 
HAVING
    CHAR_LENGTH(claves) - CHAR_LENGTH(REPLACE(claves, ',', '')) > 0;

"""

try:
    # Leer los resultados en un DataFrame de pandas
    df = pd.read_sql_query(sql_query, connection)

    # Guardar el DataFrame en un archivo Excel
    output_file = 'output_14042023.xlsx'
    df.to_excel(output_file, index=False)

    print(f"Resultados guardados en {output_file}")

finally:
    connection.close()

import pymysql
import pandas as pd

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="nnsae98n",
    db="bifsa"
)

# Consulta SQL (igual que la anterior)
sql_query = """
SELECT 
    TRIM(TRAILING ',' FROM REPLACE((CASE WHEN COUNT(pv.cve_prod) > 1 
        THEN GROUP_CONCAT(TRIM(pv.cve_prod), ',') 
        ELSE GROUP_CONCAT(TRIM(pv.cve_prod)) 
    END), ',,', ',')) AS claves,
    pv.nva_desc,
    TRIM(TRAILING ',' FROM REPLACE((CASE WHEN COUNT(pv.valores) > 1 
        THEN GROUP_CONCAT(TRIM(REPLACE(pv.valores,',',' ')), ',') 
        ELSE GROUP_CONCAT(TRIM(REPLACE(pv.valores,',',' '))) 
    END), ',,', ',')) AS valores,
    TRIM(TRAILING ',' FROM REPLACE((CASE WHEN COUNT(p.cto_ent) > 1 
        THEN GROUP_CONCAT(TRIM(p.cto_ent), ',') 
        ELSE GROUP_CONCAT(TRIM(p.cto_ent)) 
    END), ',,', ',')) AS costos
FROM 
    bifsa.new_table pv
LEFT JOIN bifsa.products p ON pv.cve_prod=p.cve_prod
WHERE
    pv.valores != 'nan' AND p.kit = 0
GROUP BY 
    pv.nva_desc 
HAVING
    CHAR_LENGTH(claves) - CHAR_LENGTH(REPLACE(claves, ',', '')) > 0;
"""

try:
    # Leer los resultados en un DataFrame de pandas
    df = pd.read_sql_query(sql_query, connection)

    # Extraer cve_prod únicas de los resultados del primer query
    cve_prod_list = []
    for row in df['claves']:
        cve_prod_list.extend(row.split(','))

    unique_cve_prod = list(set(cve_prod_list))

    # Consulta SQL para obtener productos incluidos en el primer resultado
    sql_query_included_products = """
    SELECT *
    FROM bifsa.products
    WHERE cve_prod NOT IN ('{}')
    """.format("','".join(unique_cve_prod))

    # Leer los productos incluidos en un DataFrame de pandas
    df_included_products = pd.read_sql_query(sql_query_included_products, connection)

    # Guardar el DataFrame en un archivo Excel
    output_file_included_products = 'included_products_04052023.xlsx'
    df_included_products.to_excel(output_file_included_products, index=False)

    print(f"Productos incluidos guardados en {output_file_included_products}")

finally:
    connection.close()

# -----------------------------------
import pymysql
import pandas as pd

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="nnsae98n",
    db="bifsa"
)

# Consulta SQL
sql_query = """
SELECT 
    pv.nva_desc,
    pv.cve_prod,
    pv.valores,
    p.cto_ent
FROM 
    bifsa.new_table pv
LEFT JOIN bifsa.products p ON pv.cve_prod=p.cve_prod
WHERE
    pv.valores != 'nan' AND p.kit = 0;
"""

try:
    # Leer los resultados en un DataFrame de pandas
    df = pd.read_sql_query(sql_query, connection)

    # Realizar la concatenación de comas y valores
    df['claves'] = df.groupby('nva_desc')['cve_prod'].transform(lambda x: ','.join(x))
    df['valores'] = df.groupby('nva_desc')['valores'].transform(lambda x: ','.join(x).replace(',', ' '))
    df['costos'] = df.groupby('nva_desc')['cto_ent'].transform(lambda x: ','.join(x.astype(str)))

    # Eliminar duplicados
    df = df.drop_duplicates(subset=['nva_desc'])

    # Guardar el DataFrame en un archivo Excel
    output_file = 'results/output_05062023.xlsx'
    df.to_excel(output_file, index=False)

    print(f"Resultados guardados en {output_file}")

finally:
    connection.close()

# ---------------------------------

from datetime import datetime

import pymysql
import pandas as pd

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="nnsae98n",
    db="bifsa"
)

# Consulta SQL
sql_query = """
SELECT 
    pv.nva_desc,
    pv.cve_prod,
    pv.valores,
    p.cto_ent,
    pv.sku,
    p.precc,
    p.c_prds
FROM 
    bifsa.new_table pv
LEFT JOIN bifsa.products p ON pv.cve_prod=p.cve_prod
WHERE
    pv.valores != 'nan' AND p.kit = 0 AND pv.cse_prod != 'TEMPORALES' AND pv.cse_prod != 'OBSOLETOS';
"""

try:
    # Leer los resultados en un DataFrame de pandas
    df = pd.read_sql_query(sql_query, connection)

    # Realizar la concatenación de comas y valores
    df['claves'] = df.groupby('nva_desc')['cve_prod'].transform(lambda x: ','.join(x))
    df['valores'] = df.groupby('nva_desc')['valores'].transform(lambda x: ','.join(x.str.replace(',', ' ')))
    df['costos'] = df.groupby('nva_desc')['cto_ent'].transform(lambda x: ','.join(x.astype(str)))
    df['precios3'] = df.groupby('nva_desc')['precc'].transform(lambda x: ','.join(x.astype(str)))

    # Filtrar los registros que tienen más de un cve_prod concatenado
    df_filtered = df[df['claves'].str.count(',') > 0]

    # Eliminar duplicados
    df_filtered = df_filtered.drop_duplicates(subset=['nva_desc'])
    # Obtener la fecha y hora actual
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # Guardar el DataFrame filtrado en un archivo Excel con la fecha y hora en el nombre
    output_file = f'results/output_agrupados_{timestamp}.xlsx'
    df_filtered.to_excel(output_file, index=False)

    print(f"Resultados guardados en {output_file}")

finally:
    connection.close()

# Leer el archivo de Excel
df = pd.read_excel(output_file)

# Crear una lista para almacenar los errores y el conteo de variantes
errores = []
conteo_variantes = []
conteo_valores = []
conteo_cto_ent = []
conteo_precc = []

# Recorrer cada fila del DataFrame
for index, row in df.iterrows():
    # Obtener las variantes de id y valor
    variantes_id = len(row['claves'].split(','))
    variantes_valor = len(row['valores'].split(','))

    # Verificar si el número de variantes es diferente
    if variantes_id != variantes_valor:
        errores.append(index)

    # Obtener el conteo de variantes
    conteo_variantes.append(variantes_id)
    conteo_valores.append(variantes_valor)

    # Manejar los casos en los que cto_ent es un float
    cto_ent = row['cto_ent']
    if isinstance(cto_ent, float):
        cto_ent = str(cto_ent)
        conteo_cto_ent.append(1)
    else:
        conteo_cto_ent.append(len(cto_ent.split(',')))

    # Manejar los casos en los que precc es un float
    precc = row['precc']
    if isinstance(precc, float):
        precc = str(precc)
        conteo_precc.append(1)
    else:
        conteo_precc.append(len(precc.split(',')))

# Agregar las columnas de conteo de variantes al DataFrame
df['Conteo de Variantes'] = conteo_variantes
df['Conteo de Valores'] = conteo_valores
df['Conteo de cto_ent'] = conteo_cto_ent
df['Conteo de precc'] = conteo_precc

# Crear un nuevo DataFrame solo con las filas que contienen errores
df_errores = df.loc[errores]

# Guardar el DataFrame de errores en un nuevo archivo de Excel con la fecha y hora en el nombre
errores_output_file = f'results/errores2_{timestamp}.xlsx'
df_errores.to_excel(errores_output_file, index=False)

print(f"Archivo de errores guardado en {errores_output_file}")

