import os
import random
import string
import tkinter as tk
from tkinter import filedialog

def cambiar_nombres_carpeta_rnd(carpeta_ruta):
    lista_archivos = os.listdir(carpeta_ruta)

    for nombre_archivo in lista_archivos:
        ruta_completa_antigua = os.path.join(carpeta_ruta, nombre_archivo)

        if os.path.isfile(ruta_completa_antigua):
            extension = os.path.splitext(nombre_archivo)[1]
            nuevo_nombre = ''.join(random.choices(string.ascii_lowercase, k=10)) + extension
            ruta_completa_nueva = os.path.join(carpeta_ruta, nuevo_nombre)

            try:
                os.rename(ruta_completa_antigua, ruta_completa_nueva)
                print(f"Archivo {nombre_archivo} renombrado a {nuevo_nombre}")
            except Exception as e:
                print(f"No se pudo cambiar el nombre del archivo {nombre_archivo}. Error: {e}")

def seleccionar_carpeta():
    carpeta_ruta = filedialog.askdirectory()
    etiqueta_ruta.config(text=f"Ruta de la carpeta seleccionada: {carpeta_ruta}")
    cambiar_nombres_carpeta_rnd(carpeta_ruta)

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Selector de Carpeta y Renombrador de Archivos")

# Botón para seleccionar la carpeta
boton_seleccionar = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_seleccionar.pack(pady=20)

# Etiqueta para mostrar la ruta seleccionada
etiqueta_ruta = tk.Label(ventana, text="Ruta de la carpeta seleccionada: ")
etiqueta_ruta.pack(pady=10)

# Ejecutar la ventana
ventana.mainloop()
