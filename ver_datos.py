import numpy as np

# 1. Cargar los datos desde los archivos .npy
estados = np.load('grids.npy')
etiquetas = np.load('labels.npy')

# 2. Ver la cantidad de datos generados (.shape te dice las dimensiones)
# Debería decirte (X, 8, 8), donde X es el número total de tableros guardados.
print(f"Total de tableros guardados: {estados.shape[0]}")
print(f"Total de etiquetas guardadas: {etiquetas.shape[0]}\n")

# 3. Inspeccionar un dato concreto (por ejemplo, el primer tablero guardado)
print("--- MOSTRANDO EL PRIMER TABLERO GUARDADO ---")
print(estados[1]) # Esto imprimirá la matriz de 8x8 con los 0, 1 y 2

print("\n--- ETIQUETA DE ESE TABLERO ---")
print(f"Resultado: {etiquetas[1]} (+1 Gana, -1 Pierde, 0 Empate)")

# 4. (Opcional) Ver los primeros 5 resultados de golpe
print("\nPrimeras 5 etiquetas:", etiquetas[:5])
print(len(estados))