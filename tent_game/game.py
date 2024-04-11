import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 1920
WINDOWHEIGHT = 990

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

XO = 'x'

WIDTH = 28
HEIGHT = 28
# This sets the distance between each cell
MARGIN = 2
rownum = 33
colnum = 64

grid = []
for row in range(rownum):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(colnum):
        grid[row].append(0)  # Append a cell

x_img = pygame.transform.scale(pygame.image.load("tent_game/Assets/tree.jpg"),(28,28))
o_img = pygame.transform.scale(pygame.image.load("tent_game/Assets/tent.jpg"),(28,28))

BACKGROUND = pygame.image.load('tent_game/Assets/bg.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOWWIDTH, WINDOWHEIGHT))
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Tent')

# def main():
#     while True:
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
        
#         DISPLAYSURF.blit(BACKGROUND, (0, 0))

#         pygame.display.update()
#         fpsClock.tick(FPS)
# if __name__ == '__main__':
#     main()
def main():
    DISPLAYSURF.blit(BACKGROUND, (0, 0))
    done = False
    status = None
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
                # Set the screen background
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] 
                row=  pos[1] 
                print(row)
                print(col)
                if grid[row][col] == 0:
                    if XO == 'x':
                        grid[row][col] = XO
                        XO = 'o'
                    else:
                        grid[row][col] = XO
                        XO = 'x'
        for row in range(rownum):
            for column in range(colnum):
                color = WHITE
                pygame.draw.rect(DISPLAYSURF,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
                if grid[row][column] == 'x': 
                    DISPLAYSURF.blit(x_img,((WIDTH + MARGIN)*column+2,(HEIGHT + MARGIN)*row+2))
                if grid[row][column] == 'o':
                    DISPLAYSURF.blit(o_img,((WIDTH + MARGIN)*column+2,(HEIGHT + MARGIN)*row+2))
        fpsClock.tick(FPS)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()
if __name__ == '__main__':
    main()

    