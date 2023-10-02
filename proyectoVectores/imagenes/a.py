import cv2
  
# path
  
# Reading an image in default mode
image = cv2.imread('proyectoVectores\imagenes\2.jpg')
  
# Window name in which image is displayed
  
# Using cv2.imshow() method
# Displaying the image
if image is None:
    print('Error durante la lectura de la imagen')
else:
    cv2.imshow('Imagen', image)
    cv2.waitKey(0)