import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tensorflow.keras.applications import MobileNetV2
from PIL import Image, ImageOps
#LA base de datos fue 



# Función para segmentar la imagen y guardarla como PNG
def segmentar_y_guardar_imagen(imagen_path, carpeta_destino):
    # Verificar la extensión del archivo
    ext = os.path.splitext(imagen_path)[-1].lower()

    if ext in ('.png', '.jpg', '.jpeg', '.bmp', '.pgm', '.dcm'):
        # Cargar la imagen
        if ext == '.dcm':
            import pydicom
            ds = pydicom.dcmread(imagen_path)
            image = ds.pixel_array
        else:
            image = cv2.imread(imagen_path)

        # Asegurarse de que la imagen se haya cargado correctamente
        if image is None:
            print(f"No se pudo cargar la imagen: {imagen_path}")
            return

        # Preprocesamiento de la imagen
        image = cv2.resize(image, (555, 555))
        
    
        image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(image_bw, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(contours[0])

        # Recortar la imagen original para eliminar el marco negro
        image_without_border = image[y:y + h, x:x + w]
        
        
        first_row = image_without_border[0, :]
        brightness_on_left = np.mean(first_row[:first_row.shape[0] // 2])
        brightness_on_right = np.mean(first_row[first_row.shape[0] // 2:])

        # Rotar la imagen si los píxeles claros están a la izquierda
        if brightness_on_left > brightness_on_right:
            image_without_border = np.fliplr(image_without_border)


        # Mostrar la imagen sin el marco negro
        # cv2.imshow('Imagen sin marco negro', image_without_border)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
                
        image_bw = cv2.cvtColor(image_without_border, cv2.COLOR_BGR2GRAY)     
        clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(4, 4))#
        img_clahe = clahe.apply(image_bw) + 7#Aqui aumentas el brillo
        umbral, img_bin = cv2.threshold(img_clahe, 16, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        img_dilated = cv2.dilate(img_bin, kernel, iterations=3)
        img_eroded = cv2.erode(img_dilated, kernel, iterations=6)

        # Encontrar la isla más grande
        contours, _ = cv2.findContours(img_eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        largest_island = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_island = contour

        # Crear una copia de la imagen original y dibujar la isla más grande en ella
        if largest_island is not None:
            result_image = np.zeros_like(img_eroded, dtype=np.uint8)
            cv2.drawContours(result_image, [largest_island], -1, (255), thickness=cv2.FILLED)

            # Obtener la imagen CLAHE
            result_image_with_overlay = img_clahe.copy()
            result_image_with_overlay[result_image != 0] = 255

            # Dibujar el borde en rojo
            mask = result_image.copy()
            segmented_image = cv2.bitwise_and(img_clahe, img_clahe, mask=mask)

            # Obtener el nombre del archivo sin extensión
            file_name = os.path.splitext(os.path.basename(imagen_path))[0]
            output_path = os.path.join(carpeta_destino, f"{file_name}.png")#Aqui modificar.
            # Convierte la imagen a una matriz NumPy
            
            cv2.imwrite(output_path, segmented_image)
            print(f"Imagen convertida en {output_path}")
        else:
            print("No se encontró una isla válida en la imagen")
    else:
        print(f"Extensión no admitida para la imagen: {ext}")
        
        
        


# Función para procesar una carpeta de imágenes
def procesar_carpeta_imagenes():
    root = tk.Tk()
    root.withdraw()

    # Solicitar la carpeta que contiene las imágenes
    carpeta = filedialog.askdirectory(title="Seleccionar Carpeta con Imágenes")

    if not carpeta:
        print("no se selecciono carpeta de imagenes")
        return
    

    # Solicitar la carpeta de destino
    carpeta_destino = filedialog.askdirectory(title="Seleccionar Carpeta para Guardar las Imágenes Segmentadas")

    if not carpeta_destino:
        print("no hay carpeta de destino")
        return

    # Obtener la lista de archivos en la carpeta
    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.pgm', '.dcm'))]

    for archivo in archivos:
        imagen_path = os.path.join(carpeta, archivo)
        segmentar_y_guardar_imagen(imagen_path, carpeta_destino)

# Ejecutar la función para procesar la carpeta de imágenes
procesar_carpeta_imagenes()
