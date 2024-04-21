import numpy as np
import copy
import random

from lightup.utils import *
from lightup.backtracking import backtracking_upgrade

def check_bulb_conflict(matrix):
    # check rows
    conflict = 0
    n = len(matrix)
    for i in range(n):
        bulb = 0
        for j in range(n):
            cell = matrix[i][j]
            if cell == 6:
                bulb+=1
            if cell < 6 and j == n-1:
                if bulb > 1:
                    conflict += bulb - 1
    # check cols 
    for i in range(n):
        bulb = 0
        for j in range(n):
            cell = matrix[j][i]
            if cell == 6:
                bulb+=1
            if cell < 6 and j == n-1:
                if bulb > 1:
                    conflict += bulb - 1
    return conflict

def check_black_conflict(matrix, puzzle):
    # return number on black cell - bulb conflict
    n = len(matrix)
    conflict = 0
    for key in puzzle:
        val = puzzle[key]
        if val == 5: continue
        no_bulbs_around, _ = get_total_bulb_around(key, matrix, n)
        if val != no_bulbs_around:
            conflict += abs(no_bulbs_around - val)
    
    return conflict


def caculate_fitness(matrix, puzzle):
    # caculate the fitness of current states
    # fitness = The percentage of the number of cells that are lit up, and is penal by the number of conflicts: 2
    # bulbs shining each other or the number of black adjacency is not met
    n = len(matrix)

    available_placement = 0
    for x in np.nditer(matrix): 
        if x == -2: 
            available_placement+=1

    fitness_shining_conflict = check_bulb_conflict(matrix)
    total_available_cells = n*n - len(puzzle)
    no_black_cells = len(puzzle)
    no_iluminated_cells = n*n - available_placement - no_black_cells

    fitness_black_conflict = check_black_conflict(matrix, puzzle)

    total_conflict = fitness_black_conflict + fitness_shining_conflict

    evaluation_fitness = int(100* no_iluminated_cells / total_available_cells) - total_conflict * 3

    return evaluation_fitness

def rand_normal_init(matrix, puzzle):
    # Blindly add bulbs to meet the black cell adjacency
    pass

def add_one_bulb(matrix, puzzle):
    # add a bulb and generate 10 neighbors 
    neighbours = []
    for _ in range(10):
        copy_matrix = copy.deepcopy(matrix)
        posible_pos = find_all_possible_pos(copy_matrix)
        if posible_pos == []: continue
        chosen = random.choice(posible_pos)
        place_bulb(copy_matrix ,chosen, puzzle)
        neighbours.append(copy_matrix)
    
    if neighbours == []:
        return matrix
    # get local max
    sorted(neighbours, key = lambda x: caculate_fitness(x, puzzle), reverse=True)

    return neighbours[0]

def reduce_one_bulb(matrix, puzzle):
    # remove a bulb and generate 10 neighbors 
    neighbours = []
    for _ in range(10):
        copy_matrix = copy.deepcopy(matrix)
        bulbs_pos = find_all_bulb(copy_matrix)
        if bulbs_pos == []: continue
        chosen = random.choice(bulbs_pos)
        remove_bulb(copy_matrix ,chosen,puzzle)
        neighbours.append(copy_matrix)

    if neighbours == []:
        return matrix
    # get local max
    sorted(neighbours, key = lambda x: caculate_fitness(x, puzzle), reverse=True)
    
    return neighbours[0]

def hill_climbing(matrix, puzzle):
    results = [add_one_bulb(matrix, puzzle), reduce_one_bulb(matrix, puzzle)]
    stateList2.append((matrix, results))
    
    sorted(results, key = lambda x: caculate_fitness(x, puzzle), reverse=True)

    if caculate_fitness(results[0], puzzle) < caculate_fitness(matrix, puzzle):
        results[0] = matrix

    return results[0]

def find_local_optimal(matrix, puzzle):
    copy_matrix = copy.deepcopy(matrix)

    terminate = False
    number_eval = 0
    non_fitness_improvement = 0

    local_optimal = copy_matrix
    local_optimal_fitness = caculate_fitness(local_optimal, puzzle)
    while not terminate:
        number_eval+=30

        copy_matrix = hill_climbing(copy_matrix, puzzle)
        new_fitness = caculate_fitness(copy_matrix, puzzle)

        if number_eval > 10000:
            terminate = True

        if caculate_fitness(copy_matrix, puzzle) == 100:

            terminate = True

        if local_optimal_fitness < new_fitness :
            local_optimal_fitness = new_fitness 
            local_optimal = copy_matrix
            non_fitness_improvement = 0
        else: 
            non_fitness_improvement += 1

    return local_optimal

def solve_puzzle2(matrix, puzzle):
    n = len(matrix)
    ans = []
    backtracking_upgrade(puzzle, matrix, n, 0, ans)
    ans = np.unique(ans,axis=0) #REALLY IMPORTANT!!!
    solutions = []
    for i in ans:
        a = find_local_optimal(i, puzzle)
        # print(a)
        solutions.append(a)
        # print('----------')
        # print(solutions)

    
    sorted(solutions, key = lambda x: caculate_fitness(x, puzzle), reverse=False)
    return solutions[-1]