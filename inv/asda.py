import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from jupyterthemes import jtplot
jtplot.style(theme = 'monokai', context = 'notebook', ticks = True, grid = False) 

class_names = [ 'Covid-19',  'Normal' , 'Viral Pneumonia' ]

XRay_Directory = 'D:\Practicas_Python\inv\chestData'
os.listdir(XRay_Directory)

image_generator= ImageDataGenerator(rescale= 1./255, validation_split=0.2)

train_generator=image_generator.flow_from_directory(batch_size=40,
                                                    directory= XRay_Directory,
                                                    shuffle= True,
                                                    target_size=(256,256),
                                                    class_mode= 'categorical',
                                                    subset= 'training')
train_images,train_labels= next(train_generator)
train_images.shape
train_labels.shape

L = 4
W = 4
label_names = {0 : 'Covid-19', 1 : 'Normal' , 2: 'Viral Pneumonia'}
fig, axes = plt.subplots(L, W, figsize = (12, 12))
axes = axes.ravel()

for i in np.arange(0, L*W):
    axes[i].imshow(train_images[i])
    axes[i].set_title(label_names[np.argmax(train_labels[i])])
    
    plt.subplots_adjust(wspace = 0.5)    
    
plt.show()

model = keras.Sequential([
    keras.layers.Flatten(input_shape = (28,28)),
    keras.layers.Dense(15, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
model.summary()

model.compile(optimizer=tf.keras.optimizers.legacy.RMSprop(0.0001, decay=1e-6), loss='categorical_crossentropy', metrics=['accuracy'])
