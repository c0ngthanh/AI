import pygame, sys, random
from pygame.locals import *
from enum import Enum
from tent_game.cfg import *
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
class Cell:
    def __init__(self,value : CellValue, row: int, col: int):
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
