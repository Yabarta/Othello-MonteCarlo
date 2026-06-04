import pygame
from globals import white, black
from Grid import Grid
from Node import Node
from tensorflow.keras.models import load_model

class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption('Othello')

        self.player1 = black
        self.player2 = white
        
        self.currentPlayer = black

        self.rows = 8
        self.columns = 8
        
        self.grid = Grid(self.rows, self.columns, (80, 80), self)

        self.RUN = True
        try:
            self.nn_model = load_model('modelOthello.keras')
        except:
            self.nn_model = None
        self.gameOver = False
        self.whiteCount = 0
        self.blackCount = 0
        self.resultText = ''
        self.font = pygame.font.SysFont(None, 36)
        self.modalFont = pygame.font.SysFont(None, 28)

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
                    mx, my = pygame.mouse.get_pos()
                    if self.gameOver:
                        modalW, modalH = 400, 250
                        modalX = (800 - modalW) // 2
                        modalY = (800 - modalH) // 2
                        btnW, btnH = 140, 40
                        playRect = pygame.Rect(modalX + 40, modalY + modalH - 70, btnW, btnH)
                        quitRect = pygame.Rect(modalX + modalW - 40 - btnW, modalY + modalH - 70, btnW, btnH)
                        if playRect.collidepoint((mx, my)):
                            self.reset_game()
                        elif quitRect.collidepoint((mx, my)):
                            self.RUN = False
                        continue

                    x, y = (mx - 80) // 80, (my - 80) // 80
                    validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer)
                    if not validCells:
                        pass
                    else:
                        if (y, x) in validCells:
                            self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
                            swappableTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, self.currentPlayer)
                            for tile in swappableTiles:
                                self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, tile[0], tile[1])
                            if self.currentPlayer == white:
                                self.currentPlayer = black
                            else:
                                self.currentPlayer = white

    def update(self):
        if self.gameOver:
            return

        validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer)

        if not validCells:
            if self.currentPlayer == white:
                nextPlayer = black
            else:
                nextPlayer = white
            if not self.grid.findAvailMoves(self.grid.gridLogic, nextPlayer):
                
                whites = sum(row.count(white) for row in self.grid.gridLogic)
                blacks = sum(row.count(black) for row in self.grid.gridLogic)
                self.whiteCount = whites
                self.blackCount = blacks
                if whites < blacks:
                    self.resultText = 'You win!'
                elif whites > blacks:
                    self.resultText = 'You lose.'
                else:
                    self.resultText = 'Draw.'
                self.gameOver = True
                print('Fin del juego')
                return
            else:
                print(f"El jugador {'Blanco' if self.currentPlayer == white else 'Negro'} no puede mover. Pasa turno.")
                self.currentPlayer = nextPlayer
                return

        if (self.currentPlayer == self.player2):

            validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer)
            if not validCells:
                self.currentPlayer = self.player1
                return

            rootNode = Node(grid=self.grid.gridLogic, player=self.currentPlayer, availableMoves=self.grid)

            bestMove = rootNode.UCTSearch(initialState = self.grid.gridLogic, player = self.currentPlayer, availableMoves=self.grid, iterations = 200, nn_model=self.nn_model)
        
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
        
        if self.gameOver:
            modalW, modalH = 400, 250
            modalX = (800 - modalW) // 2
            modalY = (800 - modalH) // 2
            overlay = pygame.Surface((modalW, modalH))
            overlay.set_alpha(230)
            overlay.fill((200, 200, 200))
            self.screen.blit(overlay, (modalX, modalY))
            # title
            title = self.font.render('Game Over', True, (10,10,10))
            self.screen.blit(title, title.get_rect(center=(modalX + modalW//2, modalY + 30)))
            # counts
            counts_text = f'White: {self.whiteCount}    Black: {self.blackCount}'
            counts = self.modalFont.render(counts_text, True, (10,10,10))
            self.screen.blit(counts, counts.get_rect(center=(modalX + modalW//2, modalY + 90)))
            # result
            res = self.modalFont.render(self.resultText, True, (10,10,10))
            self.screen.blit(res, res.get_rect(center=(modalX + modalW//2, modalY + 130)))
            # buttons
            btnW, btnH = 140, 40
            playRect = pygame.Rect(modalX + 40, modalY + modalH - 70, btnW, btnH)
            quitRect = pygame.Rect(modalX + modalW - 40 - btnW, modalY + modalH - 70, btnW, btnH)
            pygame.draw.rect(self.screen, (100,200,100), playRect)
            pygame.draw.rect(self.screen, (200,100,100), quitRect)
            playS = self.modalFont.render('Play Again', True, (0,0,0))
            quitS = self.modalFont.render('Quit', True, (0,0,0))
            self.screen.blit(playS, playS.get_rect(center=playRect.center))
            self.screen.blit(quitS, quitS.get_rect(center=quitRect.center))

        pygame.display.update()

    def reset_game(self):
        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        self.currentPlayer = white
        self.gameOver = False
        self.whiteCount = 0
        self.blackCount = 0
        self.resultText = ''
