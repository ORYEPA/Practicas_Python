from tensorflow import _keras
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

datos_entrenamiento = np.array([[0,0],[0,1],[1,0],[1,1]], dtype = 'float32')
datos_objetivos = np.array([[0],[1],[1],[0]], dtype = 'float32')

#print(datos_entrenamiento)
#print(datos_objetivos)

modelo = Sequential()
modelo.add(Dense(15,input_dim=2,activation='relu'))
modelo.add(Dense(1,activation='sigmoid'))

modelo.compile(loss='mean_squared_error', optimizer='adam', metrics=['binary_accuracy'])

#ENTRENAMIENTO

modelo.fit(datos_entrenamiento,datos_objetivos,epochs=100)

#PRUEBA
calif =modelo.evaluate(datos_entrenamiento,datos_objetivos)
print('%s: %.2f%%' % (modelo.metrics_names[1],calif[1]*100))