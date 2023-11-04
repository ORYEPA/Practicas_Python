import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

fm = keras.datasets.fashion_mnist
(train_images, train_labels),(test_images, test_labels)= fm.load_data()

print(train_images.shape)
print(train_labels.shape)
print(train_labels[1])

#plt.figure()
#plt.imshow(train_images[1])
#plt.colorbar()
#plt.show()

class_names = ['Camiseta','Pantalón','Suéter','Vestido',
               'Abrigo','Sandalia','Camisa','Zapatilla deportiva'
               ,'Bolso','Botines']
#print(train_images[0])

#Pre-procesamiento de datos
#Normalizar los datos
train_images = train_images/255
test_images = test_images/255

plt.figure(figsize = (10, 10))
for i in range(50):
    plt.subplot(5,10,i+1)
    plt.imshow(train_images[i],cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

#RNA
model = keras.Sequential([
    keras.layers.Flatten(input_shape = (28,28)),
    keras.layers.Dense(15, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

model.summary()

model.compile(loss='sparse_categorical_crossentropy', optimizer = 'adam', 
               metrics = ['accuracy'])

model.fit(train_images, train_labels, epochs=10)

test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Pérdida: ',test_loss)
print('Precisión: ', test_acc)

pred = model.predict(test_images)

print(pred[0])

print(np.max(pred[0]))
print(np.argmax(pred[0]))