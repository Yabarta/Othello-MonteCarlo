import pygame
from tensorflow.keras.models import load_model
from Node import Node
from Grid import Grid
from globals import white, black

class Versus:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 800), pygame.HIDDEN) 
        self.rows = 8
        self.columns = 8
        self.nn_model = load_model('modelOthello.keras')

    def jugarPartida(self, fichaIaNueva):
        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        currentPlayer = black

        if fichaIaNueva == black:
            fichaIaVieja = white
        else:
            fichaIaVieja = black
        
        while True:
            moves = self.grid.findAvailMoves(self.grid.gridLogic, currentPlayer)
            
            if not moves:
                if currentPlayer == black:
                    nextPlayer = white
                else:
                    nextPlayer = black

                if not self.grid.findAvailMoves(self.grid.gridLogic, nextPlayer):
                    break
                currentPlayer = nextPlayer
                continue

            if currentPlayer == fichaIaNueva:
                root = Node(grid=self.grid.gridLogic, player=currentPlayer, availableMoves=self.grid)
                bestMove = root.UCTSearch(initialState=self.grid.gridLogic, player=currentPlayer, availableMoves=self.grid, iterations=100, nn_model=self.nn_model)
            else:
                root = Node(grid=self.grid.gridLogic, player=currentPlayer, availableMoves=self.grid)
                bestMove = root.UCTSearch(initialState=self.grid.gridLogic, player=currentPlayer, availableMoves=self.grid, iterations=100, nn_model=None)

            if bestMove:
                y, x = bestMove
                self.grid.insertToken(self.grid.gridLogic, currentPlayer, y, x)
                swappableTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, currentPlayer)
                for tile in swappableTiles:
                    self.grid.insertToken(self.grid.gridLogic, currentPlayer, tile[0], tile[1])
            
            if currentPlayer == black:
                currentPlayer = white
            else:
                currentPlayer = black
        
        whites = sum(row.count(white) for row in self.grid.gridLogic)
        blacks = sum(row.count(black) for row in self.grid.gridLogic)

        if (blacks > whites and fichaIaNueva == black) or (whites > blacks and fichaIaNueva == white):
            return "IA Nueva"
        elif (blacks > whites and fichaIaVieja == black) or (whites > blacks and fichaIaVieja == white):
            return "IA Vieja"
        else:
            return "Empate"

if __name__ == '__main__':
    arena = Versus()
    victoriasNueva = 0
    victoriasVieja = 0
    empates = 0
    
    totalPartidas = 5
    print(f"Mejor de {totalPartidas} partidas")
    print("IA Nueva (Red Neuronal, 100 iteraciones) VS IA Vieja (MCTS Puro, 100 iteraciones)")
    
    for i in range(totalPartidas):
        if i % 2 == 0:
            color = black
            colorStr = "Negras"
        else:
            color = white
            colorStr = "Blancas"
            
        print(f"Partida {i+1} (La IA Nueva juega con {colorStr})", end=" ", flush=True)
        resultado = arena.jugarPartida(fichaIaNueva=color)
        print(f"Ganador: {resultado}")
        
        if resultado == "IA Nueva": 
            victoriasNueva += 1
        elif resultado == "IA Vieja": 
            victoriasVieja += 1
        else: 
            empates += 1
        
    print("RESULTADOS")
    print(f"IA Nueva (Red Neuronal): {victoriasNueva} victorias")
    print(f"IA Vieja (MCTS Clásico): {victoriasVieja} victorias")
    print(f"Empates:                 {empates}")
    
    if (victoriasNueva + victoriasVieja + empates) > 0:
        winRate = (victoriasNueva / (victoriasNueva + victoriasVieja + empates)) * 100
        print(f"\nWin Rate de la IA Nueva: {winRate:.2f}%")