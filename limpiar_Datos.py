import datetime
import pandas as pd

# Leer el archivo CSV
data = pd.read_excel('datos_04052023.xlsx')

# Función para extraer el texto antes de los números
def extraer_descripcion(texto):
    texto_dividido = texto.split(' ')
    descripcion = []
    for t in texto_dividido:
        if not any(c.isdigit() for c in t):
            descripcion.append(t)
        else:
            break
    return ' '.join(descripcion)

# Función para extraer el texto después de la descripción
def extraer_medidas_y_colores(texto, descripcion):
    return texto[len(descripcion):].strip()

# Aplicar las funciones a la columna 'desc_prod'
data['nva_desc'] = data['desc_prod'].apply(extraer_descripcion)
data['valores'] = data.apply(lambda row: extraer_medidas_y_colores(row['desc_prod'], row['nva_desc']), axis=1)

# Obtener la fecha y hora actual
ahora = datetime.datetime.now()

# Formatear la fecha y hora como una cadena
fecha_hora_str = ahora.strftime('%Y%m%d_%H%M%S')

# Concatenar la fecha y hora al nombre del archivo
nombre_archivo = f'datos_{fecha_hora_str}.xlsx'

# Guardar el resultado en un nuevo archivo CSV
data.to_excel(nombre_archivo, index=False)
