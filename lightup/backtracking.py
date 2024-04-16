import numpy as np
import copy
from itertools import combinations
from lightup.utils import *
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

# -2: not illuminated
# -1: illuminated
# 6: bulb
# 5: black None

def init_matrix(puzzle, size):
    matrix = np.full((size, size), fill_value=-2)
    for key in puzzle:
        i,j = key
        matrix[i][j] = puzzle[key]
    return matrix


def backtracking_upgrade(puzzle, matrix, n, counter, ans):
    # print(matrix)
    puzzle_keys = list(puzzle.keys())
    puzzle_vals = list(puzzle.values())
    # base case
    if(counter >= len(puzzle)):
        if check_condition(matrix, puzzle, n) == True:
            a = copy.deepcopy(matrix)
            ans.append(a)
            return True
    res = False

    l = puzzle_vals[counter]

    if l == 5 or l == 0:
        backtracking_upgrade(puzzle, matrix, n, counter+1 , ans)

    black_cell_pos = puzzle_keys[counter]
    num, find = get_total_bulb_around(black_cell_pos, matrix, n)
    combination = combinations(find, l-num)  


    res = False
    for comb in list(combination):
        flag = True
        for pos in comb: 
            if not valid(pos, matrix, puzzle):
                flag = False
                break
            else:
                place_bulb(matrix, pos, puzzle)
        if flag:
            res = backtracking_upgrade(puzzle, matrix, n,counter+1 , ans) or res
        
        for pos in comb:
            remove_bulb(matrix, pos, puzzle)

    return res


def backtracking(puzzle, matrix, n, stack, ans):
    
    if check_condition(matrix, puzzle, n): 
        ans.append(matrix)
        return True
        
    found_black_cell = find_black_cell(puzzle, stack)
    if found_black_cell:
        stack.append(found_black_cell)
    else: 
        return False
   
    num, find = get_total_bulb_around(stack[-1], matrix, n)
    l = puzzle[stack[-1]]
    combination = combinations(find, l-num)  
    for comb in list(combination):
        for pos in comb: 
            if not valid(pos, matrix, puzzle):
                break
            else:
                place_bulb(matrix, pos, puzzle)
        
        if backtracking(puzzle, matrix, n, stack, ans):
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
    stack = []
    ans = []
    backtracking(puzzle, matrix, 7, stack, ans)
    print('ans')


    candidate_list = get_all_cell_not_illuminated(matrix)
    while True:
        if is_solution(matrix):
            return matrix
        min_bulb += 1
        if min_bulb > n:
            print('limit exceed')
            return []
        
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

def solve_puzzle_upgrade(matrix, puzzle, n):
    # if puzzle has local mins then the previus solve_puzzle function will not work
    ans = []
    backtracking_upgrade(puzzle, matrix, n, 0, ans)
    ans = ans[0::2] #REALLY IMPORTANT!!!

    for a in ans:
        matrix = a
        candidate_list = get_all_cell_not_illuminated(matrix)
        min_bulb = 0
        while True:
            if is_solution(matrix):
                return matrix
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
                    print('found solution')
                    break