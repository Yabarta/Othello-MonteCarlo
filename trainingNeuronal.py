import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D

grids = np.load('grids.npy')
labels = np.load('labels.npy')

X = grids.reshape(-1, 8 ,8, 1).astype('float32')
Y = labels.astype('float32')

model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(8, 8, 1)),
    Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='tanh')
])

model.compile(optimizer='adam' , loss='mean_squared_error', metrics=['mae'])

model.fit(X, Y, epochs=10, batch_size=32, validation_split=0.2)

model.save('modelOthello.keras')