import pygame
import random
import copy

empty = 0
white = 1
black = 2

def loadImages(path, size):
    img = pygame.image.load(f'{path}').convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

def loadSpriteSheet(sheet, row, col, newSize, size):
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, newSize)
    image.set_colorkey('Black')
    return image

class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption('Othello')

        self.player1 = white
        self.player2 = black
        
        self.currentPlayer = white

        self.rows = 8
        self.columns = 8
        
        self.grid = Grid(self.rows, self.columns, (80, 80), self)

        self.RUN = True

    def run(self):
        while self.RUN:
            self.input()
            self.update()
            self.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.grid.printGameLogicBoard()

                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x, y = (x - 80) // 80, (y - 80) // 80
                    self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
                    if self.currentPlayer == white:
                        self.currentPlayer = black
                    else: 
                        self.currentPlayer = white

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.grid.drawGrid(self.screen)
        pygame.display.update()

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
        

class Token:
    def __init__(self, player, gridX, gridY, image, main):
        self.player = player
        self.gridX = gridX
        self.gridY = gridY
        self.posX = (80*gridY) + 80
        self.posY = (80*gridX) + 80
        self.GAME = main

        self.image = image
    
    def transition(self):
        pass

    def draw(self, window):
        window.blit(self.image, (self.posX, self.posY))


if __name__ == '__main__':
    game = Othello()
    game.run()
    pygame.quit()