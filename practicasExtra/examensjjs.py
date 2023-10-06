

# Importing the libraries that are going to be used in the program.
import tkinter as tk
from tkinter import filedialog
import numpy as np 
from matplotlib import pyplot as plt 
from PIL import Image
import cv2
from skimage import measure
from matplotlib.gridspec import GridSpec

def procesado_principal(file):
    """
    It takes an image, converts it to grayscale, then applies a series of filters to it, and finally
    displays the result.
    
    :param file: The name of the file to be processed
    """
    img=Image.open(file).convert('L')
    fig1, ax1 = plt.subplots()
    im = ax1.imshow(img)
    y = np.array(range(0))
    ax1.plot(y)
    pix_val=list(img.getdata())
    print("Maximo= ", np.max(pix_val))
    print("Minimo= ", np.min(pix_val))
    img=np.array(img)
    [n,m]=img.shape
    print(n)
    print(m)
    # Finding the number of islands in the image.
    umbral,img_bin=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    blobs_labels = measure.label(img_bin, background=0)
    print("Islas numero = ",np.max(blobs_labels))
    # A filter that is applied to the image.
    kernel = np.array(
            [[0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]], np.uint8)
    print(kernel)
    umbral,img_bw = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    print("Umbral Otsu = ", umbral)
    # A filter that is applied to the image.
    img_dilate = cv2.dilate(img_bw,kernel,iterations=15)
    blobs_labels = measure.label(img_dilate,background=0)
    print("Cantidad de islas = ", np.max(blobs_labels))
    mask = np.where(blobs_labels==1, 0,1)
    mask = np.logical_not(mask)
    img_maskor = np.copy(img)
    img_maskor[mask] = 0
    # A thresholding operation.
    ret,th1 = cv2.threshold(img_maskor,85,255,cv2.THRESH_BINARY)
    maskj = np.where(blobs_labels==1, 0,1)
    maskj = np.logical_not(th1)
    img_mask = np.copy(img_maskor)
    img_mask[maskj] = 0
    # A thresholding operation.
    ret2,th2 = cv2.threshold(img_mask,120,255,cv2.THRESH_BINARY)
    maskj = np.where(blobs_labels==1, 0,1)
    maskj = np.logical_not(th2)
    img_maskaa = np.copy(img_maskor)
    img_maskaa[maskj] = 0
    kernel2 = np.ones((6,6), np.uint8)
    # Applying a filter to the image.
    img_dilate = cv2.dilate(img_maskaa,kernel2,iterations=6)  
    maskj = np.where(blobs_labels==1, 0,1)
    maskj = np.logical_not(img_dilate)
    img_maskaa = np.copy(img_maskor)
    img_maskaa[maskj] = 0 
    # Plotting the image.
    fig, ax = plt.subplots()
    im = ax.imshow(img_maskaa)
    x = np.array(range(0))
    ax.plot(x)   
    plt.show()




def open_file_dialog():
    # """
    # It opens a file dialog and returns the path of the file selected.
    # """
    file_path = filedialog.askopenfilename()
    print(file_path)
    file=str(file_path)
    procesado_principal(file)
# Creating a button that when clicked opens a file dialog.
root = tk.Tk()
button = tk.Button(root, text="Open File", command=open_file_dialog)
button.pack()
root.mainloop()
