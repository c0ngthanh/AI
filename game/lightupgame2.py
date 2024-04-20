import time
import pygame, sys, random
from pygame.locals import *
from enum import Enum
from game.helper import *
from game.cfg import *



class LightUpGame2():
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
        # child game
        self.game1 = Grid(rownum, colnum, Cell,baseGrid)
        self.game1.SetUpLightGridCustom(OFFSET1)
        self.game2 = Grid(rownum, colnum, Cell,baseGrid)
        self.game2.SetUpLightGridCustom(OFFSET2)
        self.game3 = Grid(rownum, colnum, Cell,baseGrid)
        self.game3.SetUpLightGridCustom(OFFSET3)
        self.font = pygame.font.Font('arial.ttf', 20)
    def updateCellValue(self, row: int, col: int, value: int):
        self.game.grid[row][col].value = CellValue.int2CellValue(value)
        self.DISPLAYSURF.blit(self.tent_img, self.game.grid[row][col].position)
        pygame.display.update()
        return
    def writeText(self,grid: Grid,value: int,row,col):
        if(value not in [0,1,2,3,4]):
            return
        text = self.font.render(str(value), True,WHITE)
        renderposition = (grid.grid[row][col].position[0]+WIDTH/2,grid.grid[row][col].position[1]+HEIGHT/2)
        text_rect = text.get_rect(center=renderposition)
        self.DISPLAYSURF.blit(text, text_rect)
    def renderGrid(self,grid:Grid):
        for row in range(rownum):
            for column in range(colnum):
                pygame.draw.rect(self.DISPLAYSURF,
                            WHITE,
                            [grid.grid[row][column].position[0],
                            grid.grid[row][column].position[1],
                            WIDTH,
                            HEIGHT])
                if grid.grid[row][column].value == CellValueLight.BLACKCELL: 
                    self.DISPLAYSURF.blit(self.black_cell,grid.grid[row][column].position)
                    self.writeText(grid,grid.baseGrid[row][column],row,column)
                if grid.grid[row][column].value == CellValueLight.ILLUMINATED:
                    self.DISPLAYSURF.blit(self.yellow_cell,grid.grid[row][column].position)
                if grid.grid[row][column].value == CellValueLight.NOTILLUMINATED:
                    self.DISPLAYSURF.blit(self.white_cell,grid.grid[row][column].position)
                if grid.grid[row][column].value == CellValueLight.BULB:
                    self.DISPLAYSURF.blit(self.bulb_img,grid.grid[row][column].position)
    def placeBulb(self,r:int,c:int):
        if(self.game.grid[r][c].value == CellValueLight.BLACKCELL or self.game.grid[r][c].value == CellValueLight.BULB):
            print("Can not place bulb")
            print(r,c)
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
            print(r,c)
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
    def updateGrid(self,srcGrid,desGrid:Grid):
        for r in range(rownum):
            for c in range(colnum):
                desGrid.grid[r][c].value = CellValueLight.int2CellValue(srcGrid[r][c])
        self.renderGrid(desGrid)
        pygame.display.update()
    def run(self,grid):
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
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if(len(grid) != 0):
                #         self.updateGrid(grid[0])
                #         print("NEW")
                #         grid.pop(0)
            time.sleep(0.1)
            if(len(grid) != 0):
                self.updateGrid(grid[0],self.game1)
                # print("NEW")
                grid.pop(0)
            self.fpsClock.tick(self.FPS)
            # pygame.draw.rect(self.DISPLAYSURF,
            #                 RED,
            #                 [GetWorldPosition(-1,-1)[0],
            #                 GetWorldPosition(-1,-1)[1],
            #                 WIDTH,
            #                 HEIGHT])
                    # Go ahead and update the screen with what we've drawn.
            pygame.display.update()


    