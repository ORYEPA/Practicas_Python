import numpy as np
from PIL import Image

def cargar_imagen(ruta):
    try:
        imagen = Image.open(ruta)
        return imagen
    except:
        print("No se pudo cargar la imagen.")
        return None

def obtener_contorno(imagen):
    if imagen is None:
        return None

    imagen = imagen.convert('L')  # Convertir a escala de grises
    matriz_imagen = np.array(imagen)
    filas, columnas = matriz_imagen.shape
    contorno = np.zeros_like(matriz_imagen)

    # Algoritmo del vecino cercano (conecta 4)
    for i in range(1, filas - 1):
        for j in range(1, columnas - 1):
            vecinos = [matriz_imagen[i - 1, j], matriz_imagen[i + 1, j],
                       matriz_imagen[i, j - 1], matriz_imagen[i, j + 1]]
            valor_actual = matriz_imagen[i, j]
            if any(vecino != valor_actual for vecino in vecinos):
                contorno[i, j] = 255

    return Image.fromarray(contorno)

def main():
    ruta_imagen = input("Introduce la ruta de la imagen: ")
    imagen = cargar_imagen(ruta_imagen)
    if imagen is not None:
        contorno = obtener_contorno(imagen)
        if contorno is not None:
            contorno.show()
            contorno.save("contorno.png", "PNG")

if __name__ == "__main__":
    main()
