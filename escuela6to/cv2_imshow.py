

import cv2
import numpy as np

# Reading the image from the present directory
image = cv2.imread("D:\Practicas_Python\escuela6to/alacran_byn.png")

# Resizing the image for compatibility
image = cv2.resize(image, (400, 500))

# The initial processing of the image
image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# The declaration of CLAHE
clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(4, 4))
img_clahe = clahe.apply(image_bw) +7 #Aqui aumento se juntan islas y sucede que aumenta lo blanco

# Ordinary thresholding the same image
umbral, img_bin = cv2.threshold(img_clahe, 16, 255, cv2.THRESH_BINARY)

# Aplicar operación de dilatación para cerrar los espacios negros entre mayor mas blanco menor mas negro 
kernel = np.ones((3, 3), np.uint8)
img_dilated = cv2.dilate(img_bin, kernel, iterations=3)  # Mayor iteraciones mas negro fuera de la mama

# Aplicar operación de erosión para aislar la región de la mama, aumenta lo negro y separa 
img_eroded = cv2.erode(img_dilated, kernel, iterations=6)

# Mostrar la imagen procesada
cv2.imshow("CLAHE image", img_clahe)
cv2.imshow('Imagen blanco y negro', img_eroded)


cv2.waitKey(0)
cv2.destroyAllWindows()
