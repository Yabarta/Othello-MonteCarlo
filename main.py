import pygame
import random
import copy

empty = 0
white = 1
black = 2

class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1440,810))
        pygame.display.set_caption('Othello')

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

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.update()

class Grid:
    def __init__(self, rows, columns, size, main):
        self.GAME = main
        self.y = rows
        self.x = columns
        self.size = size

        self.gridLogic = self.regenGrid(self.y, self.x)
    
    def regenGrid(self, rows, columns):
        grid = []
        for y in range(rows):
            line = []
            for x in range(columns):
                line.append(empty)
            grid.append(line)
        
        return grid
    
    def printGameLogicBoard(self):
        print('   | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f'{item}'.center(3, " ") + '|'
            print(line)
        print()

if __name__ == '__main__':
    game = Othello()
    game.run()
    pygame.quit()