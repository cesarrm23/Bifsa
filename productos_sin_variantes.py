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
    output_file_included_products = 'included_products_14042023.xlsx'
    df_included_products.to_excel(output_file_included_products, index=False)

    print(f"Productos incluidos guardados en {output_file_included_products}")

finally:
    connection.close()
