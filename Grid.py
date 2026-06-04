import pygame
from globals import loadImages, loadSpriteSheet, empty, white, black, directions
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

        if self.GAME.currentPlayer == black:
            availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayer)
            for move in availMoves:
                pygame.draw.rect(window , 'White' , (80 + (move[1] *80) +30, 80 + (move[0] * 80) +30 , 20,20))
        
    
    def printGameLogicBoard(self):
        print('   | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f'{item}'.center(3, " ") + '|'
            print(line)

        print()

    def findValidCells(self, grid, currentPlayer):
        validCellToClick = []

        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != empty:
                        continue
                DIRECTIONS = directions(gridX, gridY)

                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkCell = grid[dirX][dirY]

                    if checkCell == 0 or checkCell == currentPlayer:
                        continue
                    if (gridX, gridY) in validCellToClick:
                        continue
                    

                    validCellToClick.append((gridX , gridY))
        return validCellToClick

    def swappableTiles(self, x,y,grid, currentPlayer ):
        surroundCells = directions(x,y)
        if len(surroundCells) == 0:
            return []
        
        swappableTiles = []

        for checkCell in surroundCells:
            checkX , checkY = checkCell
            difX, difY = checkX -x , checkY - y
            currentLine = []

            RUN = True
            while RUN:
                if grid[checkX][checkY] != currentPlayer and grid[checkX][checkY] != empty:
                    currentLine.append((checkX, checkY))
                elif grid[checkX][checkY] == currentPlayer:
                    RUN = False
                    break
                elif grid[checkX][checkY] == empty:
                    currentLine.clear()
                    RUN = False
                checkX += difX
                checkY += difY
                
                if checkX < 0 or checkX >7 or checkY < 0 or checkY > 7:
                    currentLine.clear()
                    RUN = False
            
            if len(currentLine) > 0:
                swappableTiles.extend(currentLine)
        return swappableTiles

    def findAvailMoves(self, grid, currentPlayer):
        validCells = self.findValidCells(grid, currentPlayer)
        playableCells = []

        for cell in validCells:
            x,y = cell
            if cell in playableCells:
                continue
            swapTiles = self.swappableTiles(x,y, grid, currentPlayer)

            if len(swapTiles) >0:
                playableCells.append(cell)

        return playableCells
            

                    

    def insertToken(self, grid, currentPlayer, y, x):
        tokenImg = self.whitetoken if currentPlayer == white else self.blacktoken
        self.tokens[(y,x)] = Token(currentPlayer, y, x, tokenImg, self.GAME)
        grid[y][x] = self.tokens[(y,x)].player
        