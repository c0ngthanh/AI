import time
import pygame, sys, random
from pygame.locals import *
from enum import Enum
from game.helper import *
from game.cfg import * 


class Game():
    def __init__(self,baseGrid,row_clue,col_clue,rownum,colnum):
        self.tree_img = pygame.transform.scale(pygame.image.load("game/Assets/tree.jpg"),(WIDTH,HEIGHT))
        self.tent_img = pygame.transform.scale(pygame.image.load("game/Assets/tent.jpg"),(WIDTH,HEIGHT))

        # BACKGROUND = pygame.image.load('tent_game/Assets/bg.png')
        # BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOWWIDTH, WINDOWHEIGHT))
        pygame.init()
        self.FPS = 120
        self.fpsClock = pygame.time.Clock()
        self.flag = False
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Tent')
        self.rownum = rownum
        self.colnum = colnum
        self.game = Grid(self.rownum, self.colnum, Cell,baseGrid)
        self.basegame = Grid(self.rownum, self.colnum, Cell,baseGrid)
        self.game.SetUp()
        self.basegame.SetUp()
        self.row_clue=row_clue
        self.col_clue=col_clue
        self.renderGrid(self.basegame)
        self.renderClue()
    def renderClue(self):
        font = pygame.font.Font('arial.ttf', 20)
        for i in range(len(self.row_clue)):
            text = font.render(str(self.row_clue[i]), True,WHITE)
            pos = GetWorldPosition(int(i),-1)
            renderposition = (pos[0]+WIDTH/2,pos[1]+HEIGHT/2)
            text_rect = text.get_rect(center=renderposition)
            self.DISPLAYSURF.blit(text, text_rect)
        for i in range(len(self.col_clue)):
            text = font.render(str(self.col_clue[i]), True,WHITE)
            pos = GetWorldPosition(-1,int(i))
            renderposition = (pos[0]+WIDTH/2,pos[1]+HEIGHT/2)
            text_rect = text.get_rect(center=renderposition)
            self.DISPLAYSURF.blit(text, text_rect)
        pygame.display.update()
    def updateCellValue(self, row: int, col: int, value: int):
        self.game.grid[row][col].value = CellValue.int2CellValue(value)
        self.DISPLAYSURF.blit(self.tent_img, self.game.grid[row][col].position)
        pygame.display.update()
        return
    def updateGrid(self,srcGrid,desGrid:Grid):
        for r in range(self.rownum):
            for c in range(self.colnum):
                desGrid.grid[r][c].value = CellValue.int2CellValue(srcGrid[r][c])
                if(self.basegame.grid[r][c].value == CellValue.TREE):
                    desGrid.grid[r][c].value = CellValue.TREE        
        self.renderGrid(desGrid)
        pygame.display.update()
    def renderGrid(self,grid:Grid):
        for row in range(self.rownum):
            for column in range(self.colnum):
                pygame.draw.rect(self.DISPLAYSURF,
                        WHITE,
                        [grid.grid[row][column].position[0],
                        grid.grid[row][column].position[1],
                        WIDTH,
                        HEIGHT])
                if grid.grid[row][column].value == CellValue.TENT: 
                    self.DISPLAYSURF.blit(self.tent_img,grid.grid[row][column].position)
                if grid.grid[row][column].value == CellValue.TREE:
                    self.DISPLAYSURF.blit(self.tree_img,grid.grid[row][column].position)
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
                        if(self.flag == False):
                            self.updateGrid(statelist[0], self.game)
                            statelist.pop(0)
                            self.flag = True
                        else:
                            self.flag = False
                            self.renderGrid(self.basegame)
                    # if(len(statelist) != 0):
                    #     self.updateCellValue(statelist[0][0],statelist[0][1],statelist[0][2])
                    #     statelist.pop(0)
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


    