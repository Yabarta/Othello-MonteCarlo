import numpy as np

estados = np.load('grids.npy')
etiquetas = np.load('labels.npy')

print(f"Total de tableros guardados: {len(estados)}")
print(f"Total de etiquetas guardadas: {len(etiquetas)}\n")

print("--- MOSTRANDO EL PRIMER TABLERO GUARDADO ---")
print(estados[0])

print("\n--- ETIQUETA DE ESE TABLERO ---")
print(f"Resultado: {etiquetas[0]} (+1 Gana, -1 Pierde, 0 Empate)")

print("\nPrimeras 5 etiquetas:", etiquetas[:5])