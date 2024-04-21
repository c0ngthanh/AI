from lightup.backtracking import *
from lightup.hillclimbing import *

import os
import numpy as np
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import tracemalloc

test_path = os.getcwd() + '\\lightup\\testcase'
time_checkpoint = os.getcwd() + '\\lightup\\log_time.txt'
mem_checkpoint = os.getcwd() + '\\lightup\\log_mem.txt'


class puzzle_test:
    def __init__(self, puzzle, board):
        self.puzzle = puzzle
        self.board = board
        self.size = len(board)
    def run_backtracking(self):
        solve_puzzle_upgrade(self.board, self.puzzle, self.size)
    def run_hillclimbing(self):
       solve_puzzle2(self.board, self.puzzle, False)
    def show(self):
        print(self.board)

class analyzer:
    def __init__(self):
        self.puzzle_test_list = []
        self.elapsed_time_backtracking = []
        self.elapsed_time_hillclimbing = []

        self.mem_used_backtracking = []
        self.mem_used_hillclimbing = []
        
    def load_testcases(self):
        os.chdir(test_path)
        for file in os.listdir():
            if file.endswith(".txt"):
                file_path = f"{test_path}/{file}"
                puzzle, board = self.get_puzzle(file_path)
                a = puzzle_test(puzzle, board)
                # print(file)
                self.puzzle_test_list.append(a)
        print('load testcases done')
        
        
    def get_puzzle(self, file_path):
        result = open(file_path, "r")
        size_of_board = int(result.readline())
        
        # get all black cell value and position, append them to hash map
        puzzle = {}
        for line in result.readlines():
            a = line.strip().split(' ') 
            a = [eval(i) for i in a]
            x, y, val = a[0], a[1], a[2]
            puzzle[(x,y)] = val

        matrix = init_matrix(puzzle, size_of_board)
        return puzzle, matrix
    
    def run_compare_time(self):
        print('running')
        for i in self.puzzle_test_list:
            start = timer()
            i.run_backtracking()
            end = timer()
            self.elapsed_time_backtracking.append(round(end-start, 7))

            start = timer()
            i.run_hillclimbing()
            end = timer()
            self.elapsed_time_hillclimbing.append(round(end-start, 7))

        file = open(time_checkpoint,'w')

        for i in self.elapsed_time_backtracking:
            file.write(str(i)+" ")
        
        file.write("\n")

        for i in self.elapsed_time_hillclimbing:
            file.write(str(i)+" ")
        
        file.close()
    
    def run_mem(self):
        print('running')
        for i in self.puzzle_test_list:
            tracemalloc.start()
            i.run_backtracking()
            self.mem_used_backtracking.append(round(tracemalloc.get_traced_memory()[1], 7))
            tracemalloc.stop()

            tracemalloc.start()
            i.run_hillclimbing()
            self.mem_used_hillclimbing.append(round(tracemalloc.get_traced_memory()[1], 7))
            tracemalloc.stop()

        file = open(mem_checkpoint,'w')

        for i in self.mem_used_backtracking:
            file.write(str(i)+" ")
        
        file.write("\n")

        for i in self.mem_used_hillclimbing:
            file.write(str(i)+" ")
        
        file.close()

    def plot_result(self):
        
        log_mem = open(mem_checkpoint, "r")
        backtracking_mem = log_mem.readline().strip().split(' ') 
        backtracking_mem = [eval(i) for i in backtracking_mem]
        hill_climbing_mem = log_mem.readline().strip().split(' ') 
        hill_climbing_mem = [eval(i) for i in hill_climbing_mem]
        log_mem.close()

        log_time = open(time_checkpoint, "r")
        backtracking_time = log_time.readline().strip().split(' ') 
        backtracking_time  = [eval(i) for i in backtracking_time]
        hill_climbing_time = log_time.readline().strip().split(' ') 
        hill_climbing_time  = [eval(i) for i in hill_climbing_time ]
        log_time.close()

        l = len(backtracking_time)

        # elapse time plot
        plt.subplot(1, 2, 1)
        xpoints = np.arange(l)
        plt.xticks(xpoints)
        plt.plot(xpoints,backtracking_time, label = "Backtracking")
        plt.plot(xpoints,hill_climbing_time, label = "Hill climbing")
        plt.xlabel('Testcase')
        plt.ylabel('Time(second)') 
        plt.title('Compare elapsed time')
        # memory used plot
        plt.subplot(1, 2, 2)
        plt.xticks(xpoints)
        plt.plot(xpoints,backtracking_mem, label = "Backtracking")
        plt.plot(xpoints,hill_climbing_mem, label = "Hill climbing")
        plt.xlabel('Testcase')
        plt.ylabel('Memory')
        plt.title('Compare memory usage')

        plt.legend(loc='best')
        plt.show()

a = analyzer()
# a.load_testcases()
# a.run_compare_time()
a.plot_result()


