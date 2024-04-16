import numpy as np
from game.game import *
# none = 0
# tree = 1
# tent = 2

def find_positions_to_place_tent(pos, board):
    if pos == None:
        return None, 0, 0
    # given tree position
    # find appropriate cells around the tree to place tent
    n = len(board)
    i,j = pos     
    ans = []
    #check all adjacent horizontally or vertically cells. If only 1 of them has a tent, break and return None. 
    #else return 4 cell around the tree and the position of tree
    if i - 1 >= 0:
        val = board[i-1][j]
        if val == 0 :
            ans.append([i-1,j])
    if j - 1>= 0:
        val = board[i][j-1]
        if val == 0:
            ans.append([i,j-1])
    if j + 1 < n:
        val = board[i][j+1]
        if val == 0 :
            ans.append([i,j+1])
    if i + 1 < n:
        val = board[i+1][j]
        if val == 0 :
            ans.append([i+1,j])                   
    return ans, i, j

def check_adjecent_cells(tent_pos, board):
    #return false if horizontally, vertically or even diagonally cell has a tent
    n = len(board)
    i, j = tent_pos
    if i + 1 <  n:
        #check down cell
        if board[i+1][j] == 2: return False 
        #check down left cell
        if j - 1 >= 0:
            if board[i+1][j-1] == 2: return False
        #check down right cell
        if j + 1 < n:
            if board[i+1][j+1] == 2: return False
    if i - 1 >= 0:
        #check up cell
        if board[i-1][j] == 2: return False
        #check up left cell
        if j - 1 >= 0:
            if board[i-1][j-1] == 2: return False
        #check up right cell
        if j + 1 < n:
            if board[i-1][j+1] == 2: return False
    #check right cell
    if j + 1 < n:
        if(board[i][j+1]) == 2: return False
    #check left cell
    if j - 1 >=0:
        if(board[i][j-1]) == 2: return False
    return True

def check_valid(tent_pos, board, row_clue, col_clue):
    if not check_adjecent_cells(tent_pos, board): return False
    i, j = tent_pos
    #get row
    row = board[i, :]
    #get col
    col = board[:, j]
    if( row_clue[i] < (row==2).sum()+1) or (col_clue[j] < (col==2).sum()+1):
        return False        
    return True

def is_solution(board, row_clue, col_clue):

    n = len(board)
    for i in range(n):
        row = board[i, :]
        if((row==2).sum()!= row_clue[i]): return False
        col = board[:, i]
        if((col==2).sum()!= col_clue[i]): return False
    return True

def find_tree(board, dict):
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1 and ((i,j) not in dict): return i,j
    return None

def bfs(board, row_clue, col_clue, tent, stack,statelist):
    # check stop condition
    if is_solution(board, row_clue, col_clue): 
        # print('found solution')
        return True

    stack.append(find_tree(board, stack))
    find, _, _ = find_positions_to_place_tent(stack[-1], board)
    if not find:
        if np.count_nonzero(board == 2) < tent:
            return False

        return True
    else:
        
        for pos in find:
            #check that position has adjecent tent or not
            if check_valid(pos, board, row_clue, col_clue):
                board[pos[0]][pos[1]] = 2
                statelist.append((pos[0],pos[1],2))
                if bfs(board, row_clue, col_clue, tent,  stack,statelist):
                    return True
            
                board[pos[0]][pos[1]] = 0
                statelist.append((pos[0],pos[1],0))
                stack.pop(-1)
    return False
