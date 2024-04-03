import numpy as np
import math
from random import randint, random
from tent.bfs import is_solution
from tent.utils.utils import *

class sa:
    def __init__(self, board, row_clue, col_clue):
        self.map_tree_tent = {}
        self.state = board
        self.row_clue = row_clue
        self.col_clue = col_clue
        self.no_of_tree = (board == 1).sum()

    def init_state(self):
        stack = []
        while find_tree(self.state, stack):
            tree_pos = find_tree(self.state, stack)
            stack.append(tree_pos)
            find, _, _ = find_positions_to_place_tent(stack[-1], self.state)
            n  = len(find)
            a = find[randint(0, n-1)]
            self.state[a[0],a[1]]  = 2

            self.map_tree_tent[tree_pos] = a
        print('init state:')
        print(self.state)
        
    def eval(candidate, self):
        # count total number of row clue and col clue satisfied
        n = len(candidate)
        eval = 0
        for i in range(n):
            row = candidate[i, :]
            col = candidate[:, i]
            if (row==2).sum() != self.row_clue[i]:
                eval +=1
            if (col==2).sum() != self.col_clue[i]:
                eval+=1
        return eval
    
    def random_neighbour(self):
        pass

    def schedule(t):
        pass

    def neighbour_operator(self):
        print('after neighbour operator')
        n = randint(0, self.no_of_tree - 1)
       
        l =  list(self.map_tree_tent.keys())
        tree_pos = l[n]
        tent_pos = self.map_tree_tent[tree_pos]
        self.state[tent_pos[0]][tent_pos[1]] = 0

        print(tree_pos)
        print(self.state)
        
        cells_around_tree = []
        i, j = tree_pos
        if i - 1 >= 0:
            if check_adjecent_cells([i-1, j],self.state):
                cells_around_tree.append([i-1, j])
        if i + 1 < n:
            if check_adjecent_cells([i+1, j],self.state):
                cells_around_tree.append([i+1, j])
        if j - 1 >= 0:
            if check_adjecent_cells([i, j-1],self.state):
                cells_around_tree.append([i, j-1])
        if j + 1 < n:
            if check_adjecent_cells([i, j+1],self.state):
                cells_around_tree.append([i, j+1])    
        
        if len(cells_around_tree) <= 0: return
        n = randint(0, len(cells_around_tree)-1)
        new_tent_pos = cells_around_tree[n]
        print(new_tent_pos)
        i, j = new_tent_pos
        self.state[i][j] = 2
        print(self.state)

    def run(self):
        self.init_state()
        self.neighbour_operator()





    

def neighbourhood_operator(state, no_of_tent):
    #choose a random tent, move it to a cell such that still paired with the tree
    #neighbourhood operator must ensure the criterion that each tree should be paired with 1 tree
    n = randint(0, no_of_tent-1)
    print(n)
    stack = []
    while n >= 0:
        pos = find_tent(state, stack)
        stack.append(pos)
        n-=1
    pos = stack[-1]
    i, j = pos
    state[i][j] = 0
    
    print(state)

    n = len(state)
    stack = []
    if i - 1 >= 0:
        if j - 1 >= 0:
            if check_adjecent_cells([i-1, j-1],state):
                stack.append([i-1, j-1])
        if j + 1 < n:
            if check_adjecent_cells([i-1, j+1],state):
                stack.append([i-1, j+1])

    if i + 1 < n:
        if j - 1 >= 0:
            if check_adjecent_cells([i+1, j-1],state):
                stack.append([i+1, j-1])
        if j + 1 < n:
            if check_adjecent_cells([i+1, j+1],state):
                stack.append([i+1, j+1])    
    if len(stack) <= 0: return
    n = randint(0, len(stack)-1)
    new_tent_pos = stack[n]
    i, j = new_tent_pos 
    state[i][j] = 2

    print(state)



# def sa_algorithm(state, row_clue, col_clue):
#     while not is_solution(state, row_clue, col_clue):
#         T = schedule(t)
#         if T == 0: 
#             return state
#         candidate = random_neighbour(state, row_clue, col_clue)
#         e = eval(candidate) - eval(state)
#         if e > 0:
#             state = candidate
#         else:
#             prob = probability(E, T)
#             if random() < prob:
#                 state = candidate