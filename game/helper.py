import pygame, sys, random
from pygame.locals import *
from enum import Enum
from game.cfg import *
import numpy as np


def GetWorldPosition(row:int,col:int):
    return (OFFSET[0]+(MARGIN + WIDTH) * col + MARGIN, OFFSET[1]+(MARGIN + HEIGHT) * row + MARGIN)
class CellValue(Enum):
    NOTHING = 0
    TREE = 1
    TENT = 2
    def int2CellValue(value: int):
        if(value == 0):
            return CellValue.NOTHING
        if(value == 1):
            return CellValue.TREE
        if(value == 2):
            return CellValue.TENT
class CellValueLight(Enum):
    NOTILLUMINATED = -2
    ILLUMINATED = -1
    BLACKCELL = [0,1,2,3,4,5]
    # BLACK1 = 1
    # BLACK2 = 2
    # BLACK3 = 3
    # BLACK4 = 4
    # BLACKNONE = 5
    BULB = 6
    def int2CellValue(value: int):
        if(value == -2):
            return CellValueLight.NOTILLUMINATED
        if(value == -1):
            return CellValueLight.ILLUMINATED
        if(value in [0,1,2,3,4,5]):
            return CellValueLight.BLACKCELL
        # if(value == 1):
        #     return CellValueLight.BLACK1
        # if(value == 2):
        #     return CellValueLight.BLACK2
        # if(value == 3):
        #     return CellValueLight.BLACK3
        # if(value == 4):
        #     return CellValueLight.BLACK4
        # if(value == 5):
        #     return CellValueLight.BLACKNONE
        if(value == 6):
            return CellValueLight.BULB
class Cell:
    def __init__(self,value, row: int, col: int):
        self.value = value
        self.row = row
        self.col = col
        self.position = GetWorldPosition(row,col)
class Grid:
    def __init__(self, rowNum:int, colNum:int,cell,baseGrid: np.ndarray):
        self.row = rowNum
        self.col = colNum
        self.grid = []
        self.baseGrid = baseGrid
        self.cellClass = cell
    def SetUp(self):
        for r in range(self.row):
            self.grid.append([])
            for c in range(self.col):
                cell = Cell(CellValue.int2CellValue(self.baseGrid[r][c]),r,c)
                self.grid[r].append(cell)
    def SetUpLightGrid(self):
        for r in range(self.row):
            self.grid.append([])
            for c in range(self.col):
                cell = Cell(CellValueLight.int2CellValue(self.baseGrid[r][c]),r,c)
                self.grid[r].append(cell)
