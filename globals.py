import pygame

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
