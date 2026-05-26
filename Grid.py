import pygame
from globals import loadImages, loadSpriteSheet, empty, white, black
from Token import Token

class Grid:
    def __init__(self, rows, columns, size, main):
        self.GAME = main
        self.y = rows
        self.x = columns
        self.size = size
        self.whitetoken = loadImages('images/white.png', size)
        self.blacktoken = loadImages('images/black.png', size)
        self.bg = self.loadBackgroundImages()

        self.tokens = {}

        self.gridBg = self.createBgImg()

        self.gridLogic = self.regenGrid(self.y, self.x)
    
    def loadBackgroundImages(self):
        alpha = 'ABCDFEGHI'
        spriteSheet = pygame.image.load('images/board.png').convert_alpha()
        imageDict = {}
        for i in range(3):
            for j in range(7):
                imageDict[alpha[j]+str(i)] = loadSpriteSheet(spriteSheet, j, i, (self.size), (32, 32))
        return imageDict
    
    def createBgImg(self):
         # Números son 1 para las columnnas bordes, 2 para la última fila y 0 para el resto.
         # Letras son C y E para las columnas bordes, D para las filas borde y A y B se alternan en el centro como un tablero de ajedrez.
         gridBg = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'F0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'F1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'F1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'F1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'F1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'F1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'F1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'F1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'F1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'F2'],
        ]
         image = pygame.Surface((960, 960))
         for j, row in enumerate(gridBg):
             for i, img in enumerate(row):
                 image.blit(self.bg[img], (i * self.size[0], j * self.size[1])) 
         return image
       
    
    def regenGrid(self, rows, columns):
        grid = []
        for y in range(rows):
            line = []
            for x in range(columns):
                line.append(empty)
            grid.append(line)
        self.insertToken(grid, white, 3, 3)
        self.insertToken(grid, black, 3, 4)
        self.insertToken(grid, white, 4, 4)
        self.insertToken(grid, black, 4, 3)
        
        return grid
    
    def drawGrid(self, window):
        window.blit(self.gridBg, (0, 0))

        for token in self.tokens.values():
            token.draw(window)
    
    def printGameLogicBoard(self):
        print('   | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f'{item}'.center(3, " ") + '|'
            print(line)
        print()

    def insertToken(self, grid, currentPlayer, y, x):
        tokenImg = self.whitetoken if currentPlayer == white else self.blacktoken
        self.tokens[(y,x)] = Token(currentPlayer, y, x, tokenImg, self.GAME)
        grid[y][x] = self.tokens[(y,x)].player
        