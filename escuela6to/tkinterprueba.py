

import tkinter as tk
from tkinter import filedialog
 
import numpy as np #importe de libreria
from matplotlib import pyplot as plt #pa plotear
from PIL import Image
import cv2
from skimage import measure

def procesado_principal(file):
    img=Image.open(file).convert('L')
    fig1, ax1 = plt.subplots()
    im = ax1.imshow(img)#figura 1
   
    y = np.array(range(0))
    ax1.plot(y)
    pix_val=list(img.getdata())
    print("Maximo= ", np.max(pix_val))
    print("Minimo= ", np.min(pix_val))
    img=np.array(img)
    [n,m]=img.shape
    print(n)
    print(m)
    bw_img=np.zeros(img.shape)

    for i in range(n):
        for j in range(m):
            if img[i,j]>200:
                bw_img[i,j]=1
            else:
                bw_img[i,j]=0
    # plt.imshow(bw_img,cmap='gray')
    umbral,img_bin=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # plt.imshow(img_bin,cmap='gray')

    blobs_labels = measure.label(img_bin, background=0)

    # plt.imshow(blobs_labels, cmap="nipy_spectral")
    print("Islas numero = ",np.max(blobs_labels))
    # plt.axis("off")

    kernel = np.ones((3,3), np.uint8)
    print(kernel)
    img_eroded = cv2.erode(img_bin, kernel, iterations=2)
    # plt.imshow(img_eroded, cmap="gray")
    # plt.axis("off")
    umbral,img_bw = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    print("Umbral Otsu = ", umbral)
    # plt.imshow(img_bw,cmap="gray")
    kernel = np.ones((5,5),np.uint8)
    print(kernel)
    img_dilate = cv2.dilate(img_bw,kernel,iterations=5)
    # plt.imshow(img_dilate,cmap="gray")
    blobs_labels = measure.label(img_dilate,background=0)
    print("Cantidad de islas = ", np.max(blobs_labels))
    # plt.axis("off")
    mask = np.where(blobs_labels==1, 0,1)
    mask = np.logical_not(mask)
    img_mask = np.copy(img)
    img_mask[mask] = 0
    # plt.imshow(img_mask)
    # plt.axis("off")
    fig, ax = plt.subplots()
    im = ax.imshow(img_mask)
    x = np.array(range(0))
    ax.plot(x)
    plt.show()




def open_file_dialog():
    file_path = filedialog.askopenfilename()
    print(file_path)
    file=str(file_path)
    procesado_principal(file)
root = tk.Tk()

button = tk.Button(root, text="Open File", command=open_file_dialog)
button.pack()

root.mainloop()
