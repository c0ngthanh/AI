import numpy as np

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
    # if pos == None:
    #     return 0, []
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
        # print('there is no bulb here')
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

def find_all_bulb(matrix):
    n = len(matrix)
    bulbs_pos = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 6:
                bulbs_pos.append((i,j))

    return bulbs_pos

def find_all_possible_pos(matrix):
    n = len(matrix)
    posible_pos = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == -2:
               posible_pos.append((i,j))

    return posible_pos