import pygame, sys, random
from pygame.locals import *
from enum import Enum

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

OFFSET = [0,0]

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
rownum = 7
colnum = 7


x_img = pygame.transform.scale(pygame.image.load("tent_game/Assets/tree.jpg"),(28,28))
o_img = pygame.transform.scale(pygame.image.load("tent_game/Assets/tent.jpg"),(28,28))

# BACKGROUND = pygame.image.load('tent_game/Assets/bg.png')
# BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOWWIDTH, WINDOWHEIGHT))
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Tent')

class CellValue(Enum):
    NOTHING = 0
    TENT = 1
    TREE = 2
class Cell:
    def __init__(self,value : CellValue, position: tuple):
        self.value = value
        self.position = position
class Grid:
    def __init__(self, rowNum:int, colNum:int,cell):
        self.row = rowNum
        self.col = colNum
        self.grid = []
        self.cellClass = cell
    def SetUp(self):
        for r in range(self.row):
            self.grid.append([])
            for c in range(self.col):
                self.grid[r].append(self.cellClass(CellValue.NOTHING, (0,0)))
grid = Grid(rownum, colnum, Cell)
grid.SetUp()

def main():
    # DISPLAYSURF.blit(BACKGROUND, (0, 0))
    done = False
    status = None
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
                # Set the screen background
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     col = pos[0] 
            #     row=  pos[1] 
            #     print(row)
            #     print(col)
            #     if grid[row][col] == 0:
            #         if XO == 'x':
            #             grid[row][col] = XO
            #             XO = 'o'
            #         else:
            #             grid[row][col] = XO
            #             XO = 'x'
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
        for row in range(rownum):
            for column in range(colnum):
                color = BLACK
                pygame.draw.rect(DISPLAYSURF,
                                WHITE,
                                [OFFSET[0]+(MARGIN + WIDTH) * column + MARGIN,
                                OFFSET[1]+(MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
                if grid.grid[row][column].value == CellValue.TENT: 
                    DISPLAYSURF.blit(x_img,(OFFSET[0]+(WIDTH + MARGIN)*column+2,OFFSET[1]+(HEIGHT + MARGIN)*row+2))
                if grid.grid[row][column].value == CellValue.TREE:
                    DISPLAYSURF.blit(o_img,(OFFSET[0]+(WIDTH + MARGIN)*column+2,OFFSET[1]+(HEIGHT + MARGIN)*row+2))
        fpsClock.tick(FPS)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.update()
if __name__ == '__main__':
    main()

    