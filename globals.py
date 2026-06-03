import pygame

empty = 0
white = 1
black = 2
MCTSConstant = 1.414

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

def directions(x , y , minX= 0 , minY =0, maxX= 7, maxY = 7):
    validDirections = []
    #Todas las dirreecciones hacia arriba
    if x != minX: validDirections.append((x-1,y))
    if x != minX and y != minY: validDirections.append((x-1,y-1))
    if x != minX and y!= maxY: validDirections.append((x-1,y+1))

    #Todas las dirreecciones hacia abajo
    if x != maxX: validDirections.append((x+1,y))
    if x != maxX and y != minY: validDirections.append((x+1,y-1))
    if x != maxX and y != maxY: validDirections.append((x+1,y+1))

    #Izquierda y derecha
    if y != minY: validDirections.append((x,y-1))
    if y != maxY: validDirections.append((x,y+1))

    return validDirections