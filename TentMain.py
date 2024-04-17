import numpy as np
from tent.bfs import bfs
from tent.sa import *
from game.game import *
puzzle =  """
            001000
            000010
            000001  
            100000
            000100
            010001
        """
row_clue =  """
                111112    
            """
col_clue =  """
                111121    
            """

def puzzle_to_np_array(board, row, col):
    puzzle   = np.array([[int(i) for i in line] for line in board.split()])
    row_clue = [int (i) for i in row.split()[0]]
    col_clue = [int (i) for i in col.split()[0]]
    size = len(col_clue)
    return puzzle, row_clue, col_clue, size
x, y ,z, n = puzzle_to_np_array(puzzle, row_clue, col_clue)
stack =  [] 
statelist = []
game = Game(x,y,z)
bfs(x, y, z, n, stack,statelist)
game.run(statelist)
# print(x)

# a = sa(x, y, z)
# a.run()

