import numpy as np
import copy
from itertools import combinations
from game.lightupgame import *


"""
backtracking idea

1. check end condition, if is_solution return
2. loop through all black cells, if number of adjecent bulbs not smaller than the number on a black cells,
append that black cell to stack A
3. get a candidate cell
4. if valid, place bulb to that cell, append to stack B 
5. call backtraking
6. remove bulb
7. check end condition, if not is solution
    - find cell that has val == -2
    - if valid, place bulb
    - call back tracking
    remove bulb


"""


puzzle = {
    (0,1): 0,
    (1,6): 3,
    (2,2): 2,
    (2,4): 2,
    (4,2): 1,
    (4,4): 5,
    (5,0): 5,
    (6,5): 0
}

# -2: not illuminated
# -1: illuminated
# 6: bulb
# 5: black None
from enum import Enum

class Symbol(Enum):
    o = 8

def init_matrix(puzzle, size):
    matrix = np.full((size, size), fill_value=-2)
    for key in puzzle:
        i,j = key
        matrix[i][j] = puzzle[key]
    return matrix

def is_solution(matrix):
    for x in np.nditer(matrix): 
        if x == -2: 
            return False
    return True
    
def check_condition(matrix, puzzle, n):
    for key in puzzle:
        if puzzle[key] == 5 : continue
        num, _ = get_total_bulb_around(key, matrix, n)
        if puzzle[key] != num: return False

    return True

def get_black_neighbour(puzzle, position, n):
    cells = []
    i, j = position
    if i -1 >=0:
        if (i-1,j) in puzzle : cells.append((i-1,j))
    if j - 1 >= 0:
        if (i, j-1) in puzzle : cells.append((i, j-1))
    if i + 1 < n:
        if (i+1, j) in puzzle :  cells.append((i+1,j))
    if j+1< n:
        if (i, j+1) in puzzle: cells.append((i,j+1))

    return cells
    # and puzzle[(i-1,j)] == 0

def valid(position, matrix, puzzle):
    # check valid to place a bulb at pos (position)
    n = len(matrix)
    i, j = position
    if matrix[i][j] == 8: return False
    # check adjacent cells
    adjacents = get_black_neighbour(puzzle, position, n)
    for pos in adjacents:
       black_val = puzzle[pos]
       no_bulbs, _ = get_total_bulb_around(pos, matrix,n)
       if (black_val <  no_bulbs + 1):
            return False

    return True

def get_total_bulb_around(pos, matrix, n):
    empty_cells = [] #cells that has not be iluminated around black cell
    count = 0
    i, j = pos 
    if i -1 >=0:
        if matrix[i-1,j] == 6 : count+=1
        elif matrix[i-1,j] == -2: empty_cells.append((i-1,j)) 
    if j - 1 >= 0:
        if matrix[i,j-1] == 6 : count+=1
        elif matrix[i,j-1] == -2: empty_cells.append((i,j-1)) 
    if i + 1 < n:
        if matrix[i+1,j] == 6 : count+=1
        elif matrix[i+1,j] == -2: empty_cells.append((i+1,j)) 
    if j+1< n:
        if matrix[i,j+1] == 6 : count+=1
        elif matrix[i,j+1] == -2: empty_cells.append((i,j+1)) 

    return count, empty_cells
  


def place_bulb(matrix, position, puzzle):

    i, j = position
    n = len(matrix)
    if (i,j) not in puzzle:
        # place bulb
        matrix[i][j] = 6
        # illuminate up cells
        for k in range(i-1, -1, -1):
            #check if cell[k][j] is black cell
            if (k, j) in puzzle:
                break
            else: 
                matrix[k][j] = 9 if matrix[k][j] == 8 else 8 
        # illuminate down cells
        for k in range(i+1, n):
            #check if cell[k][j] is black cell
            if (k, j) in puzzle:
                break
            else: 
                matrix[k][j] = 9 if matrix[k][j] == 8 else 8 
        # illuminate left cells
        for k in range(j-1, -1, -1):
            #check if cell[k][j] is black cell
            if (i, k) in puzzle:
                break
            else: 
                matrix[i][k] = 9 if matrix[i][k] == 8 else 8 
        # illuminate down cells
        for k in range(j+1, n):
            #check if cell[k][j] is black cell
            if (i, k) in puzzle:
                break
            else: 
                matrix[i][k] = 9 if matrix[i][k] == 8 else 8 

def remove_bulb(matrix, pos, puzzle):
    n = len(matrix)
    i, j = pos
    if (matrix[i][j] != 6):
        print('there is no bulb here')
        return False
    matrix[i][j] = -2

    for k in range(i-1, -1, -1):
    #check if cell[k][j] is black cell
        if (k, j) in puzzle:
            break
        else: 
            matrix[k][j] = 8 if matrix[k][j] == 9 else -2 
    # unilluminate down cells
    for k in range(i+1, n):
        #check if cell[k][j] is black cell
        if (k, j) in puzzle:
            break
        else: 
            matrix[k][j] = 8 if matrix[k][j] == 9 else -2 
    # unilluminate left cells
    for k in range(j-1, -1, -1):
        #check if cell[k][j] is black cell
        if (i, k) in puzzle:
            break
        else: 
            matrix[i][k] = 8 if matrix[i][k] == 9 else -2 
    # unilluminate down cells
    for k in range(j+1, n):

        if (i, k) in puzzle:
            break
        else: 
            matrix[i][k] = 8 if matrix[i][k] == 9 else -2 
    return True

res = []
def get_min():
    solution = float('inf')

    for i in res:
        if solution > i[0]:
            solution = i[0]

    return solution

def find_pos_2_place_bulb(matrix, stack):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == -2 : 
                return (i,j)
    return -99, -99

def find_candidate_pos(matrix, puzzle):
    n = len(matrix)
    for key in puzzle:
        if puzzle[key] == 0: continue
        no_bulbs, empty_cell = get_total_bulb_around(key, matrix, n)
        if  no_bulbs < puzzle[key]:
            return empty_cell
    return None

def find_black_cell(puzzle, stack):
    for key in puzzle:
        if key not in stack and puzzle[key] != 0 and puzzle[key] != 5:
            return key
    return None

def backtracking(puzzle, matrix, n, stack):
    if check_condition(matrix, puzzle, n): 
        return True 
    
    stack.append(find_black_cell(puzzle, stack))
    num, find = get_total_bulb_around(stack[-1], matrix, n)
    l = puzzle[stack[-1]]
    combination = combinations(find, l-num)  
    for comb in list(combination):
        for pos in comb: 
            if not valid(pos, matrix, puzzle):
                break
            else:
                place_bulb(matrix, pos, puzzle)
        
        if backtracking(puzzle, matrix, n, stack):
            return True
        
        for pos in comb:
            remove_bulb(matrix, pos, puzzle)

        stack.pop(-1)
    
    return False
        

def get_all_cell_not_illuminated(matrix):
    res = []
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == -2:
                res.append((i,j))
    return res


def solve_puzzle(matrix, puzzle, min_bulb, n):
    candidate_list = get_all_cell_not_illuminated(matrix)
    while True:
        if is_solution(matrix):
            print(min_bulb, matrix)
            return
        min_bulb += 1
        if min_bulb > n:
            print('limit exceed')
            break
        
        all_combination = combinations(candidate_list, min_bulb)
        copy_matrix = copy.deepcopy(matrix)
        for comb in list(all_combination):
            for pos in comb:
                if valid(pos, copy_matrix, puzzle):
                    place_bulb(copy_matrix, pos, puzzle)
                else:
                    break
            if is_solution(copy_matrix): 
                matrix = copy_matrix
                break

if __name__ == "__main__":
    stack = []
    matrix = init_matrix(puzzle, 7)
    print(matrix)
    # game = LightUpGame(matrix)
    # game.run()
    backtracking(puzzle, matrix, 7, stack)
    # # print(matrix)
    # # print('second phase')
    solve_puzzle(matrix, puzzle, 0, 7)
    # # print('???')
    print(matrix)


# place_bulb(matrix, (4,2), puzzle)
# print()
# print(matrix)