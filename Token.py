import pygame

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
