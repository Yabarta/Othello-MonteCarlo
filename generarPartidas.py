from Node import Node
from Grid import Grid
from globals import white, black
import numpy as np
import copy
import pygame
from tensorflow.keras.models import load_model

class PartidaSimulada:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 800), pygame.HIDDEN)

        self.rows = 8
        self.columns = 8
        
        self.grid = Grid(self.rows, self.columns, (80, 80), self)

        self.nn_model = load_model('modelOthello.keras')

    def jugarPartida(self):
        grids = []
        turns = []
        currentPlayer = white

        while True:
            moves = self.grid.findAvailMoves(self.grid.gridLogic , currentPlayer)
            
            if not moves:
                if currentPlayer == black:
                    nextPlayer = white
                else:
                    nextPlayer = black
                if not self.grid.findAvailMoves(self.grid.gridLogic, nextPlayer):
                    break
                else:
                    currentPlayer = nextPlayer
                    continue
            
            relativeGrid = np.zeros((8, 8))
            for fila in range(8):
                for col in range(8):
                    if self.grid.gridLogic[fila][col] == currentPlayer:
                        relativeGrid[fila][col] = 1 
                    elif self.grid.gridLogic[fila][col] != 0:
                        relativeGrid[fila][col] = 2
            
            grids.append(relativeGrid)
            turns.append(currentPlayer)

            root = Node(grid=self.grid.gridLogic, player=currentPlayer , availableMoves=self.grid)
            bestMove = root.UCTSearch(initialState=self.grid.gridLogic, player=currentPlayer, availableMoves=self.grid, iterations=500)

            if bestMove:
                y, x = bestMove
                self.grid.insertToken(self.grid.gridLogic, currentPlayer, y, x)
                swappableTiles = self.grid.swappableTiles(y,x ,self.grid.gridLogic , currentPlayer)
                for tile in swappableTiles:
                    self.grid.insertToken(self.grid.gridLogic, currentPlayer, tile[0], tile[1])
            
            if currentPlayer == black:
                currentPlayer = white
            else:
                currentPlayer = black
        
        whites = sum(row.count(white) for row in self.grid.gridLogic)
        blacks = sum(row.count(black) for row in self.grid.gridLogic)

        if whites > blacks:
            winner = white
        elif whites < blacks:
            winner = black
        else:
            winner = 0
        
        labels = []
        for turn in turns:
            if winner == 0: labels.append(0)
            elif turn == winner: labels.append(1)
            else: labels.append(-1)
        
        return grids, labels
    
if __name__ == '__main__':
    all_grids = []
    all_labels = []

    for i in range(200):
        game = PartidaSimulada()
        grid , label = game.jugarPartida()
        all_grids.extend(grid)
        all_labels.extend(label)
    
    np.save('grids.npy', np.array(all_grids))
    np.save('labels.npy', np.array(all_labels))