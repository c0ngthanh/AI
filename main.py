import numpy as np
from tent.bfs import bfs
from tent.sa import *
puzzle =  """
            000010
            001000
            011000
            000000
            000001
            001010
        """
row_clue =  """
                201202    
            """
col_clue =  """
                102103    
            """

def puzzle_to_np_array(board, row, col):
    puzzle   = np.array([[int(i) for i in line] for line in board.split()])
    row_clue = [int (i) for i in row.split()[0]]
    col_clue = [int (i) for i in col.split()[0]]
    size = len(col_clue)
    return puzzle, row_clue, col_clue, size

x, y ,z, n = puzzle_to_np_array(puzzle, row_clue, col_clue)
stack =  [] 
# bfs(x, y, z, n, stack)
# print(x)

a = sa(x, y, z)
a.run()

