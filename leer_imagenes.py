import cv2
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cargar la imagen de la nota de compra
imagen = cv2.imread('nota_compra.jpg')

# Preprocesar la imagen (opcional)
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar OCR a la imagen
texto = pytesseract.image_to_string(imagen_gris)

# Procesar el texto extraído para obtener el total
resultado = re.search(r'\d+\.\d+', texto)
total = resultado.group() if resultado else None

# Mostrar el total
if total:
    print("Total:", total)
else:
    print("No se encontró el total en la nota de compra.")
