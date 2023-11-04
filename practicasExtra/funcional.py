

# Importing the libraries that are going to be used in the program.
import tkinter as tk
from tkinter import filedialog
import numpy as np 
from matplotlib import pyplot as plt 
from PIL import Image
import cv2
from skimage import measure
from matplotlib.gridspec import GridSpec

    ###
    # It takes an image, converts it to grayscale, then applies a threshold to it, then erodes it, then
    # dilates it, then applies a mask to it, then applies a threshold to it, then applies an adaptive
    # threshold to it, then plots the original image and the processed image
    
    # :param file: The name of the file to be processed
    ###
def procesado_principal(file):
    img=Image.open(file).convert('L')
    # Getting the data from the image and then printing the maximum and minimum values of the image.
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
    kernel = np.ones((15,15), np.uint8)
    print(kernel)
   
    umbral,img_bw = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    print("Umbral Otsu = ", umbral)
   # Dilating the image and then finding the number of islands in the image.
    img_dilate = cv2.dilate(img_bw,kernel,iterations=2)
    blobs_labels = measure.label(img_dilate,background=0)
    print("Cantidad de islas = ", np.max(blobs_labels))
    # Creating a mask that is going to be applied to the image.
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
    
    
    # Applying a threshold to the image.
    ret,th1 = cv2.threshold(img_mask,110,255,cv2.THRESH_BINARY)
    ret2,th2 = cv2.threshold(img_mask2,110,255,cv2.THRESH_BINARY)
    ret3,th3 = cv2.threshold(img_mask3,110,255,cv2.THRESH_BINARY)
    
    # Applying an adaptive threshold to the image.
    # tg1 = cv2.adaptiveThreshold(th1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,11,2)
    # tg2 = cv2.adaptiveThreshold(th2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,11,2)
    # tg3 = cv2.adaptiveThreshold(th3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,11,2)
    
    img_eroded = cv2.erode(img_bin, kernel, iterations=2)
   
    blobs_labels2 = measure.label(img_eroded,background=0)
    print("Cantidad de islas = ", np.max(blobs_labels2))
    plt.axis("off")
    maske1 = np.where(blobs_labels2==1, 0,1)
    maske1 = np.logical_not(maske1)
    img_maske = np.copy(img)
    img_maske[maske1] = 0
    maske2 = np.where(blobs_labels2==0, 1,1)
    maske2= np.logical_not(maske2)
    img_maske2 = np.copy(img)
    img_maske2[maske2] = 0
    maske3 = np.where(blobs_labels2==1,1,0)
    maske3= np.logical_not(maske3)
    img_maske3 = np.copy(img)
    img_maske3[maske3] = 0
    # Creating a grid of 4 rows and 3 columns.
    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(4, 3, figure=fig)
    img=Image.open(file).convert('L') 
    axs = fig.add_subplot(gs[0, :])
    axs.set_title('Imagen Original')
    axs.imshow(img,'gray')
    titles = ['Mascara Dilatacion','Mascara Dilatacion','Mascara Dilatacion','Mascara','Mascara','Mascara','Mascara','Mascara','Mascara']
    
    # Creating a list of images and then plotting them in a grid.
    images = [img_mask,img_mask2,img_mask3,th1 ,th2,th3,img_maske,img_maske2,img_maske3]
    for i in range(9):
        ax = fig.add_subplot(gs[i+3])
        ax.set_title(titles[i])
        ax.imshow(images[i],'gray',vmin=0,vmax=255)
    fig.align_labels() 
        
       
   
   
    
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
