import pygame
from tensorflow.keras.models import load_model
from Node import Node
from Grid import Grid
from globals import white, black

class Torneo:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 800), pygame.HIDDEN) 
        self.rows = 8
        self.columns = 8
        
        print("Cargando red neuronal...")
        self.nn_model = load_model('modelOthello.keras')

    def jugar_partida(self, color_ia_nueva):
        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        current_player = black
        color_ia_vieja = white if color_ia_nueva == black else black
        
        while True:
            moves = self.grid.findAvailMoves(self.grid.gridLogic, current_player)
            
            if not moves:
                next_player = white if current_player == black else black
                if not self.grid.findAvailMoves(self.grid.gridLogic, next_player):
                    break # Fin del juego
                current_player = next_player
                continue

            # --- DECISIÓN DEL MOVIMIENTO ---
            if current_player == color_ia_nueva:
                # IA NUEVA (Red Neuronal con pocas iteraciones)
                root = Node(grid=self.grid.gridLogic, player=current_player, availableMoves=self.grid)
                bestMove = root.UCTSearch(initialState=self.grid.gridLogic, player=current_player, availableMoves=self.grid, iterations=100, nn_model=self.nn_model)
            else:
                # IA VIEJA (MCTS Clásico con muchas iteraciones)
                root = Node(grid=self.grid.gridLogic, player=current_player, availableMoves=self.grid)
                bestMove = root.UCTSearch(initialState=self.grid.gridLogic, player=current_player, availableMoves=self.grid, iterations=100, nn_model=None)
            # -------------------------------

            if bestMove:
                y, x = bestMove
                self.grid.insertToken(self.grid.gridLogic, current_player, y, x)
                swappableTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, current_player)
                for tile in swappableTiles:
                    self.grid.insertToken(self.grid.gridLogic, current_player, tile[0], tile[1])
            
            current_player = white if current_player == black else black
        
        # Contar resultados finales
        whites = sum(row.count(white) for row in self.grid.gridLogic)
        blacks = sum(row.count(black) for row in self.grid.gridLogic)

        if (blacks > whites and color_ia_nueva == black) or (whites > blacks and color_ia_nueva == white):
            return "IA Nueva"
        elif (blacks > whites and color_ia_vieja == black) or (whites > blacks and color_ia_vieja == white):
            return "IA Vieja"
        else:
            return "Empate"

if __name__ == '__main__':
    arena = Torneo()
    victorias_nueva = 0
    victorias_vieja = 0
    empates = 0
    
    total_partidas = 5
    print(f"\n--- INICIANDO TORNEO AL MEJOR DE {total_partidas} PARTIDAS ---")
    print("IA Nueva (Red Neuronal, 50 iteraciones) VS IA Vieja (Aleatorio, 500 iteraciones)")
    print("-" * 50)
    
    for i in range(total_partidas):
        # Alternar quién empieza jugando (quién lleva las negras)
        if i % 2 == 0:
            color = black
            color_str = "Negras"
        else:
            color = white
            color_str = "Blancas"
            
        print(f"Partida {i+1} (La IA Nueva juega con {color_str})...", end=" ", flush=True)
        resultado = arena.jugar_partida(color_ia_nueva=color)
        print(f"Ganador: {resultado}")
        
        if resultado == "IA Nueva": victorias_nueva += 1
        elif resultado == "IA Vieja": victorias_vieja += 1
        else: empates += 1
        
    print("\n" + "=" * 30)
    print("      RESULTADOS FINALES      ")
    print("=" * 30)
    print(f"IA Nueva (Red Neuronal): {victorias_nueva} victorias")
    print(f"IA Vieja (MCTS Clásico): {victorias_vieja} victorias")
    print(f"Empates:                 {empates}")
    
    if (victorias_nueva + victorias_vieja) > 0:
        win_rate = (victorias_nueva / (victorias_nueva + victorias_vieja)) * 100
        print(f"\nWin Rate de la IA Nueva: {win_rate:.2f}%")