

import tkinter as tk
from tkinter import filedialog
 
import numpy as np #importe de libreria
from matplotlib import pyplot as plt #pa plotear
from PIL import Image
import cv2
from skimage import measure
from matplotlib.gridspec import GridSpec

def procesado_principal(file):
    img=Image.open(file).convert('L')
    # fig1, ax1 = plt.subplots()
    # im = ax1.imshow(img)
    # y = np.array(range(0))
    # ax1.plot(y)
    
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

    kernel = np.ones((10,10), np.uint8)
    print(kernel)
    img_eroded = cv2.erode(img_bin, kernel, iterations=2)
    # plt.imshow(img_eroded, cmap="gray")
    # plt.axis("off")
    umbral,img_bw = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    print("Umbral Otsu = ", umbral)
    # plt.imshow(img_bw,cmap="gray")
    
    img_dilate = cv2.dilate(img_bw,kernel,iterations=5)
    # plt.imshow(img_dilate,cmap="gray")
    blobs_labels = measure.label(img_dilate,background=0)
    print("Cantidad de islas = ", np.max(blobs_labels))
    # plt.axis("off")
    mask1 = np.where(blobs_labels==1, 0,1)
    mask1 = np.logical_not(mask1)
    img_mask = np.copy(img)
    img_mask[mask1] = 0
    mask2 = np.where(blobs_labels==0, 1,1)
    mask2= np.logical_not(mask2)
    img_mask2 = np.copy(img)
    img_mask2[mask2] = 0
    mask3 = np.where(blobs_labels==1,1,0)
    mask3= np.logical_not(mask3)
    img_mask3 = np.copy(img)
    img_mask3[mask3] = 0
    
    
    ret,th1 = cv2.threshold(img_mask,90,255,cv2.THRESH_BINARY)
    ret2,th2 = cv2.threshold(img_mask2,90,255,cv2.THRESH_BINARY)
    ret3,th3 = cv2.threshold(img_mask3,90,255,cv2.THRESH_BINARY)
    
    # tg1 = cv2.adaptiveThreshold(th1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,11,2)
    # tg2 = cv2.adaptiveThreshold(th2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,11,2)
    # tg3 = cv2.adaptiveThreshold(th3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,11,2)
    maskj = np.where(blobs_labels==1, 0,1)
    maskj = np.logical_not(th1)
    img_mask = np.copy(img_mask)
    img_mask[maskj] = 0
    mask2j = np.where(blobs_labels==0, 1,1)
    mask2j= np.logical_not(th2)
    img_mask2j = np.copy(img_mask2)
    img_mask2j[mask2j] = 0
    mask3j = np.where(blobs_labels==1,1,0)
    mask3j= np.logical_not(th3)
    img_mask3j = np.copy(img_mask3)
    img_mask3j[mask3j] = 0
    
    
    

    
    fig = plt.figure(constrained_layout=True)

    gs = GridSpec(4, 3, figure=fig)
    img=Image.open(file).convert('L') 
    axs = fig.add_subplot(gs[0, :])
    axs.imshow(img,'gray')
    
    images = [img_mask,img_mask2,img_mask3,th1 ,th2,th3,img_mask,img_mask2j,img_mask3j]
    for i in range(9):
        ax = fig.add_subplot(gs[i+3])
        ax.imshow(images[i],'gray',vmin=0,vmax=255)
        # ax.set_ylabel('YLabel1 %d' % i)
        # ax.set_xlabel('XLabel1 %d' % i)
   
    fig.align_labels()  # same as fig.align_xlabels(); fig.align_ylabels()
        
       
   
   
    
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
