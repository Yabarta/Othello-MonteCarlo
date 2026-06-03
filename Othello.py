import pygame
from globals import white, black
from Grid import Grid
from Node import Node

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
                    validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer)
                    if not validCells:
                        pass
                    else:
                        if (y,x) in validCells:
                            self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
                            swappableTiles = self.grid.swappableTiles(y,x ,self.grid.gridLogic , self.currentPlayer)
                            for tile in swappableTiles:
                                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, tile[0], tile[1])
                            if self.currentPlayer == white:
                                self.currentPlayer = black
                            else: 
                                self.currentPlayer = white

    def update(self):
        if (self.currentPlayer == self.player2):
            bestMove = Node.UCTSearch(initialState = self.grid.gridLogic, player = self.currentPlayer, availableMoves=self.grid, iterations = 500)
        
            if bestMove:
                y, x = bestMove
                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
                swappableTiles = self.grid.swappableTiles(y,x ,self.grid.gridLogic , self.currentPlayer)
                for tile in swappableTiles:
                    self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, tile[0], tile[1])
            
            self.currentPlayer = self.player1
            

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.grid.drawGrid(self.screen)
        pygame.display.update()
