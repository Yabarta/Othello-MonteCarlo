import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# Función para multiplicar los datos x8 usando las simetrías del Othello
def augment_data_with_symmetries(grids, labels):
    augmented_grids = []
    augmented_labels = []
    
    for g, l in zip(grids, labels):
        for i in range(4):
            # Rotaciones de 0, 90, 180 y 270 grados
            rot_g = np.rot90(g, i)
            augmented_grids.append(rot_g)
            augmented_labels.append(l)
            
            # Espejo horizontal de cada rotación
            flip_g = np.fliplr(rot_g)
            augmented_grids.append(flip_g)
            augmented_labels.append(l)
            
    return np.array(augmented_grids), np.array(augmented_labels)

# 1. Cargar datos base
grids = np.load('grids.npy')
labels = np.load('labels.npy')
print(f"Datos originales cargados: {grids.shape[0]} estados de tablero.")

# 2. Aplicar Aumento de Datos (Simetrías)
grids_aug, labels_aug = augment_data_with_symmetries(grids, labels)
print(f"Datos aumentados por simetría: {grids_aug.shape[0]} estados de tablero (Multiplicado x8).")

# 3. Formatear dimensiones
X = grids_aug.reshape(-1, 8, 8, 1).astype('float32')
Y = labels_aug.astype('float32')

# 4. MEZCLA ALEATORIA (Crucial para corregir la validación y evitar el Data Leakage)
indices = np.arange(X.shape[0])
np.random.shuffle(indices)
X = X[indices]
Y = Y[indices]

# 5. Arquitectura de red mejorada (Un poco más profunda y con Dropout contra el Overfitting)
model = Sequential([
    Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(8, 8, 1)),
    Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
    Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same'),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),  # Ayuda a que la red no memorice jugadas exactas de memoria
    Dense(1, activation='tanh')
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# 6. Early Stopping para detener el entrenamiento si deja de mejorar en la validación
early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Reducimos las épocas máximas a 20 porque ahora hay muchos más datos combinados
model.fit(
    X, Y, 
    epochs=20, 
    batch_size=64, 
    validation_split=0.15, 
    callbacks=[early_stop]
)

# 7. Guardar modelo mejorado
model.save('modelOthello.keras')
print("¡Modelo entrenado y guardado como 'modelOthello.keras'!")