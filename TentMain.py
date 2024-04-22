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
# Memory Min Conflict 
ram_usage_mc = []
# Memory Backtracking
ram_usage_btk = []

for i in range(len(puzzle)):
    x, y ,z, n = puzzle_to_np_array(puzzle[i], row_clue[i], col_clue[i])
    statelist = []
    stack =  [] 
    # # Min-Conflict
    print("Min-Conflict:")
    a = mc(x, y, z, n)
    tracemalloc.start()
    a.run()
    # Memory
    ram_usage_mc.append(round(tracemalloc.get_traced_memory()[1], 7))
    tracemalloc.stop()
    # Time
    run_time1, run_time2 = a.runtime()
    run_time.append(run_time1)
    all_run_time.append(run_time2)

    # Backtracking
    # print("Backtracking:")
    game = Game(x,y,z,n,n)
    tracemalloc.start()
    start_time = time.time()
    bfs(x, y, z, n, stack)
    end_time = time.time()
    # Time
    run_time3 = round(1000*(end_time - start_time),4)
    btk_runtime.append(run_time3)
    # Memory
    ram_usage_btk.append(round(tracemalloc.get_traced_memory()[1], 7))
    tracemalloc.stop()
    print(x)
    print(a.stateList)
    game.run(a.stateList)


#Testcase
x = [1,2,3,4,5,6,7,8,9,10]
# #Draw plot
Time_plot(x, run_time, all_run_time, btk_runtime)
Mem_plot(x, ram_usage_mc, ram_usage_btk)
