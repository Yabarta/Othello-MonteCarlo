import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Dropout
from tensorflow.keras.callbacks import EarlyStopping

def augmentDataWithSymmetries(grids, labels):
    augmentedGrids = []
    augmentedLabels = []
    
    for g, l in zip(grids, labels):
        for i in range(4):
            rotG = np.rot90(g, i)
            augmentedGrids.append(rotG)
            augmentedLabels.append(l)
            
            flipG = np.fliplr(rotG)
            augmentedGrids.append(flipG)
            augmentedLabels.append(l)
            
    return np.array(augmentedGrids), np.array(augmentedLabels)

grids = np.load('grids.npy')
labels = np.load('labels.npy')
print(f"Datos originales cargados: {grids.shape[0]} estados de tablero.")

gridsAug, labelsAug = augmentDataWithSymmetries(grids, labels)
print(f"Datos aumentados por simetría: {gridsAug.shape[0]} estados de tablero (Multiplicado x8).")

inputX = gridsAug.reshape(-1, 8, 8, 1).astype('float32')
targetY = labelsAug.astype('float32')

indices = np.arange(inputX.shape[0])
np.random.shuffle(indices)
inputX = inputX[indices]
targetY = targetY[indices]

model = Sequential([
    Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(8, 8, 1)),
    Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
    Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='tanh')
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

earlyStop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

model.fit(
    inputX, targetY, 
    epochs=20, 
    batch_size=64, 
    validation_split=0.15, 
    callbacks=[earlyStop]
)

model.save('modelOthello.keras')
print("¡Modelo entrenado y guardado como 'modelOthello.keras'!")