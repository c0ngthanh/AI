import time
import pygame, sys, random
from pygame.locals import *
from enum import Enum
from game.helper import *
from game.cfg import * 


class Game():
    def __init__(self,baseGrid,row_clue,col_clue):
        self.tree_img = pygame.transform.scale(pygame.image.load("game/Assets/tree.jpg"),(WIDTH,HEIGHT))
        self.tent_img = pygame.transform.scale(pygame.image.load("game/Assets/tent.jpg"),(WIDTH,HEIGHT))

        # BACKGROUND = pygame.image.load('tent_game/Assets/bg.png')
        # BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOWWIDTH, WINDOWHEIGHT))
        pygame.init()
        self.FPS = 120
        self.fpsClock = pygame.time.Clock()

        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Tent')

        self.game = Grid(rownum, colnum, Cell,baseGrid)
        self.game.SetUp()
        self.row_clue=row_clue
        self.col_clue=col_clue
        self.renderClue()
    def renderClue(self):
        font = pygame.font.Font('arial.ttf', 20)
        for i in range(len(self.row_clue)):
            text = font.render(str(self.row_clue[i]), True,WHITE)
            pos = GetWorldPosition(int(i),-1)
            textRect = pygame.Rect(pos[0],pos[1],WIDTH,HEIGHT)
            self.DISPLAYSURF.blit(text, textRect.center)
        for i in range(len(self.col_clue)):
            text = font.render(str(self.col_clue[i]), True,WHITE)
            pos = GetWorldPosition(-1,int(i))
            textRect = pygame.Rect(pos[0],pos[1],WIDTH,HEIGHT)
            self.DISPLAYSURF.blit(text, textRect.center)
        pygame.display.update()
    def updateCellValue(self, row: int, col: int, value: int):
        self.game.grid[row][col].value = CellValue.int2CellValue(value)
        self.DISPLAYSURF.blit(self.tent_img, self.game.grid[row][col].position)
        pygame.display.update()
        return
    def run(self,statelist:list):
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
                    if(len(statelist) != 0):
                        self.updateCellValue(statelist[0][0],statelist[0][1],statelist[0][2])
                        statelist.pop(0)
                    # print(statelist)
            for row in range(rownum):
                for column in range(colnum):
                    color = BLACK
                    pygame.draw.rect(self.DISPLAYSURF,
                            WHITE,
                            [self.game.grid[row][column].position[0],
                            self.game.grid[row][column].position[1],
                            WIDTH,
                            HEIGHT])
                    if self.game.grid[row][column].value == CellValue.TENT: 
                        self.DISPLAYSURF.blit(self.tent_img,self.game.grid[row][column].position)
                    if self.game.grid[row][column].value == CellValue.TREE:
                        self.DISPLAYSURF.blit(self.tree_img,self.game.grid[row][column].position)
            # time.sleep(0.001)
            # self.updateCellValue(statelist[0][0],statelist[0][1],statelist[0][2])
            # statelist.pop(0)
            self.fpsClock.tick(self.FPS)
            # pygame.draw.rect(self.DISPLAYSURF,
            #                 RED,
            #                 [GetWorldPosition(-1,-1)[0],
            #                 GetWorldPosition(-1,-1)[1],
            #                 WIDTH,
            #                 HEIGHT])
                    # Go ahead and update the screen with what we've drawn.
            pygame.display.update()


    