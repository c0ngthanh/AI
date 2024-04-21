import numpy as np
import time
import sys
import matplotlib.pyplot as plt
from tent.bfs import bfs
from tent.mc import *
from tent.test import *
from game.game import *
from game.cfg import *

def puzzle_to_np_array(board, row, col):
    puzzle   = np.array([[int(i) for i in line] for line in board.split()])
    row_clue = [int (i) for i in row.split('.')]
    col_clue = [int (i) for i in col.split('.')]
    size = len(col_clue)
    return puzzle, row_clue, col_clue, size
def SetStateList(value):
    statelist = value
# Run time by min conflict
run_time = []
all_run_time = []
# Run time by backtracking
btk_runtime = []
for i in range(len(puzzle)):
    x, y ,z, n = puzzle_to_np_array(puzzle[i], row_clue[i], col_clue[i])
    statelist = []
    stack =  [] 
    # # Min-Conflict
    print("Min-Conflict:")
    a = mc(x, y, z, n)
    a.run()
    mem1 = sys.getsizeof(a.run())
    run_time1, run_time2 = a.runtime()
    print("Run time of best trial by min conflict:", run_time1, "ms")
    print("Run time of all trial by min conflict:", run_time2, "ms")

    # # Memory
    # print("Memory usage Min Conflict:", mem1, "bytes")

    # Backtracking
    # print("Backtracking:")
    game = Game(x,y,z,n,n)
    # start_time = time.time()
    # # mem2 = sys.getsizeof(bfs(x, y, z, n, stack,statelist))
    # bfs(x, y, z, n, stack,statelist)
    # end_time = time.time()
    # print(x)
    # run_time3 = round(1000*(end_time - start_time),4)
    # print("Run time by backtracking:", run_time3, "ms")
    print(a.stateList)
    game.run(a.stateList)
    # Memory
    # print("Memory usage Backtracking:", mem2, "bytes")
#     run_time.append(run_time1)
#     all_run_time.append(run_time2)
#     btk_runtime.append(run_time3)

# #Draw plot
# x = [1,2,3,4,5,6,7,8,9,10]

# # Draw 3 line
# plt.plot(x, run_time, label='Min Conflict', color='b', linestyle='-', linewidth=2) 
# plt.plot(x, all_run_time, label='Total time Min Conflict', color='g', linestyle='--', linewidth=2) 
# plt.plot(x, btk_runtime, label='Backtracking', color='r', linestyle='-.', linewidth=2) 

# # Add info
# plt.title("Tent puzzle")
# plt.xlabel("Testcase")
# plt.ylabel("Time (ms)")
# plt.legend()
# plt.show()
