import pandas as pd

# Leer los archivos de Excel
file_laguna = "PRECIOS_LAGUNA.xlsx"
file_monterrey = "PRECIOS_MTY.xlsx"

df_laguna = pd.read_excel(file_laguna)
df_monterrey = pd.read_excel(file_monterrey)

# Realizar la comparativa de precios (preca, precb, precc, precd, prece, precf)
precios = ['preca', 'precb', 'precc', 'precd', 'prece', 'precf']

# Creamos una lista para almacenar los resultados de cada comparativa
resultados = []

for precio in precios:
    # Seleccionamos las columnas relevantes para la comparación y creamos copias explícitas
    df_laguna_prec = df_laguna[['cve_prod', 'desc_prod', precio]].copy()
    df_monterrey_prec = df_monterrey[['cve_prod', 'desc_prod', precio]].copy()

    # Renombramos la columna de precios para identificar su origen en los DataFrames copiados
    df_laguna_prec.rename(columns={precio: f'preco_laguna_{precio}'}, inplace=True)
    df_monterrey_prec.rename(columns={precio: f'preco_monterrey_{precio}'}, inplace=True)

    # Unimos los dataframes por la columna 'cve_prod' utilizando how='inner'
    merged_df = pd.merge(df_laguna_prec, df_monterrey_prec, on='cve_prod', how='inner')

    # Verificamos si hay diferencias en los precios de ambos archivos
    merged_df[f'diferencia_{precio}'] = merged_df[f'preco_laguna_{precio}'] != merged_df[f'preco_monterrey_{precio}']

    # Filtramos solo los productos con diferencias en los precios
    productos_con_diferencias = merged_df[merged_df[f'diferencia_{precio}']]

    # Agregamos los resultados a la lista
    resultados.append(productos_con_diferencias)

# Concatenamos los resultados en un solo dataframe
resultados_completos = pd.concat(resultados, axis=1)

# Guardamos los resultados en un nuevo archivo Excel
result_file_name = "resultados_comparativa_precios.xlsx"
result_file_path = "results/" + result_file_name

resultados_completos.to_excel(result_file_path, index=False, engine='openpyxl')
print(f"Los resultados se han guardado en '{result_file_path}'")
