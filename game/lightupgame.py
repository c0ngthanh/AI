import time
import pygame, sys, random
from pygame.locals import *
from enum import Enum
from game.helper import *
from game.cfg import * 


class LightUpGame():
    def __init__(self,baseGrid):
        pygame.init()
        self.FPS = 120
        self.fpsClock = pygame.time.Clock()

        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Light UP Game')
        # BACKGROUND = pygame.image.load('tent_game/Assets/bg.png')
        # BACKGROUND = pygame.transform.scale(BACKGROUND, (WINDOWWIDTH, WINDOWHEIGHT))
        self.bulb_img = pygame.transform.scale(pygame.image.load("game/Assets/bulb.jpg"),(WIDTH,HEIGHT))
        self.red_bulb_img = pygame.transform.scale(pygame.image.load("game/Assets/redbulb.jpg"),(WIDTH,HEIGHT))
        self.black_cell = pygame.transform.scale(pygame.image.load("game/Assets/black_cell.png"),(WIDTH,HEIGHT))
        self.white_cell = pygame.transform.scale(pygame.image.load("game/Assets/bg.png"),(WIDTH,HEIGHT))
        self.yellow_cell = pygame.transform.scale(pygame.image.load("game/Assets/yellow.jpg"),(WIDTH,HEIGHT))


        self.game = Grid(rownum, colnum, Cell,baseGrid)
        self.game.SetUpLightGrid()
        self.font = pygame.font.Font('arial.ttf', 20)
        # self.row_clue=row_clue
        # self.col_clue=col_clue
        # self.renderClue()
    # def renderClue(self):
    #     font = pygame.font.Font('arial.ttf', 20)
    #     for i in range(len(self.row_clue)):
    #         text = font.render(str(self.row_clue[i]), True,WHITE)
    #         pos = GetWorldPosition(int(i),-1)
    #         textRect = pygame.Rect(pos[0],pos[1],WIDTH,HEIGHT)
    #         self.DISPLAYSURF.blit(text, textRect.center)
    #     for i in range(len(self.col_clue)):
    #         text = font.render(str(self.col_clue[i]), True,WHITE)
    #         pos = GetWorldPosition(-1,int(i))
    #         textRect = pygame.Rect(pos[0],pos[1],WIDTH,HEIGHT)
    #         self.DISPLAYSURF.blit(text, textRect.center)
    #     pygame.display.update()
    def updateCellValue(self, row: int, col: int, value: int):
        self.game.grid[row][col].value = CellValue.int2CellValue(value)
        self.DISPLAYSURF.blit(self.tent_img, self.game.grid[row][col].position)
        pygame.display.update()
        return
    def writeText(self,value: int,row,col):
        if(value not in [0,1,2,3,4]):
            return
        text = self.font.render(str(value), True,WHITE)
        renderposition = (self.game.grid[row][col].position[0]+WIDTH/2,self.game.grid[row][col].position[1]+HEIGHT/2)
        text_rect = text.get_rect(center=renderposition)
        self.DISPLAYSURF.blit(text, text_rect)
    def initGrid(self):
        for row in range(rownum):
            for column in range(colnum):
                color = BLACK
                pygame.draw.rect(self.DISPLAYSURF,
                            WHITE,
                            [self.game.grid[row][column].position[0],
                            self.game.grid[row][column].position[1],
                            WIDTH,
                            HEIGHT])
                if self.game.grid[row][column].value == CellValueLight.BLACKCELL: 
                    self.DISPLAYSURF.blit(self.black_cell,self.game.grid[row][column].position)
                    self.writeText(self.game.baseGrid[row][column],row,column)
                if self.game.grid[row][column].value == CellValueLight.ILLUMINATED:
                    self.DISPLAYSURF.blit(self.yellow_cell,self.game.grid[row][column].position)
                if self.game.grid[row][column].value == CellValueLight.NOTILLUMINATED:
                    self.DISPLAYSURF.blit(self.white_cell,self.game.grid[row][column].position)
                if self.game.grid[row][column].value == CellValueLight.BULB:
                    self.DISPLAYSURF.blit(self.bulb_img,self.game.grid[row][column].position)
    def placeBulb(self,r:int,c:int):
        if(self.game.grid[r][c].value == CellValueLight.BLACKCELL or self.game.grid[r][c].value == CellValueLight.BULB):
            print("Can not place bulb")
            return
        self.game.grid[r][c].value = CellValueLight.BULB
        self.game.grid[r][c].numoflight = self.game.grid[r][c].numoflight + 1
        self.DISPLAYSURF.blit(self.bulb_img,self.game.grid[r][c].position)
        # Update row and column cell
        for i in range(r+1,colnum):
            if(self.game.grid[i][c].value == CellValueLight.BLACKCELL):
                break
            self.updateNewBulbGrid(i,c,True)
        for i in range(r-1,-1,-1):
            if(self.game.grid[i][c].value == CellValueLight.BLACKCELL):
                break
            self.updateNewBulbGrid(i,c,True)
        for i in range(c+1,rownum):
            if(self.game.grid[r][i].value == CellValueLight.BLACKCELL):
                break
            self.updateNewBulbGrid(r,i,True)
        for i in range(c-1,-1,-1):
            if(self.game.grid[r][i].value == CellValueLight.BLACKCELL):
                break
            self.updateNewBulbGrid(r,i,True)
        pygame.display.update()
    def removeBulb(self,r:int,c:int):
        if(self.game.grid[r][c].value != CellValueLight.BULB):
            print("Can not remove bulb")
            return
        self.game.grid[r][c].numoflight = self.game.grid[r][c].numoflight - 1
        if(self.game.grid[r][c].numoflight == 0):
            self.game.grid[r][c].value = CellValueLight.NOTILLUMINATED
            self.DISPLAYSURF.blit(self.white_cell,self.game.grid[r][c].position)
        else:
            self.game.grid[r][c].value = CellValueLight.ILLUMINATED
            self.DISPLAYSURF.blit(self.yellow_cell,self.game.grid[r][c].position)
        # Update row and column cell
        for i in range(r+1,colnum):
            if(self.game.grid[i][c].value == CellValueLight.BLACKCELL):
                break
            self.updateNewBulbGrid(i,c,False)
        for i in range(r-1,-1,-1):
            if(self.game.grid[i][c].value == CellValueLight.BLACKCELL):
                break
            self.updateNewBulbGrid(i,c,False)
        for i in range(c+1,rownum):
            if(self.game.grid[r][i].value == CellValueLight.BLACKCELL):
                break
            self.updateNewBulbGrid(r,i,False)
        for i in range(c-1,-1,-1):
            if(self.game.grid[r][i].value == CellValueLight.BLACKCELL):
                break
            self.updateNewBulbGrid(r,i,False)
        pygame.display.update()
    def updateNewBulbGrid(self,r:int,c:int, addBulb:bool):
        if(addBulb):
            if(self.game.grid[r][c].value == CellValueLight.NOTILLUMINATED):
                self.game.grid[r][c].value = CellValueLight.ILLUMINATED
                self.game.grid[r][c].numoflight = 1
                self.DISPLAYSURF.blit(self.yellow_cell,self.game.grid[r][c].position)
            elif(self.game.grid[r][c].value == CellValueLight.BULB):
                self.DISPLAYSURF.blit(self.red_bulb_img,self.game.grid[r][c].position)
                self.game.grid[r][c].numoflight = self.game.grid[r][c].numoflight + 1
            elif(self.game.grid[r][c].value == CellValueLight.ILLUMINATED):
                self.game.grid[r][c].numoflight = self.game.grid[r][c].numoflight + 1
            # print(r,c,self.game.grid[r][c].numoflight)
        else:
            if(self.game.grid[r][c].value == CellValueLight.ILLUMINATED):
                self.game.grid[r][c].numoflight = self.game.grid[r][c].numoflight-1
                if(self.game.grid[r][c].numoflight == 0):
                    self.game.grid[r][c].value = CellValueLight.NOTILLUMINATED
                    self.DISPLAYSURF.blit(self.white_cell,self.game.grid[r][c].position)

            if(self.game.grid[r][c].value == CellValueLight.BULB):
                self.game.grid[r][c].numoflight = self.game.grid[r][c].numoflight-1
                if(self.game.grid[r][c].numoflight == 1):
                    self.DISPLAYSURF.blit(self.bulb_img,self.game.grid[r][c].position)
                else:
                    self.DISPLAYSURF.blit(self.red_bulb_img,self.game.grid[r][c].position)
    def run(self):
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
                    self.placeBulb(3,2)
                    self.placeBulb(1,2)
                    # self.placeBulb(1,2)
                    # print(statelist)
                if event.type == pygame.KEYDOWN:
            # checking if key "A" was pressed
                    if event.key == pygame.K_a:
                        self.removeBulb(1,2)
                    if event.key == pygame.K_d:
                        self.removeBulb(3,2)
                # if pygame.key.get_pressed == K_UP:
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


    