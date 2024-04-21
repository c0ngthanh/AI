from lightup.backtracking import *
from lightup.hillclimbing import *
from game.lightupgame import *
from game.lightupgame2 import *
from lightup import utils

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
# puzzle = {
#     (0,2): 5,
#     (0,4): 2,
#     (1,4): 1,
#     (2,0): 1,
#     (2,1): 5,
#     (2,6): 5,
#     (3,3): 1,
#     (4,0): 1,
#     (4,5): 1,
#     (4,6): 5,
#     (5,2): 0,
#     (6,2): 1,
#     (6,4): 1
# }
if __name__ == "__main__":
    utils.resetState()
    matrix = init_matrix(puzzle, 7)
    # hill climbing
    game = LightUpGame2(matrix,puzzle)
    game.renderGrid(game.game)
    game.renderGrid(game.game1)
    game.renderGrid(game.game2)
    game.renderGrid(game.game3)
    matrix = solve_puzzle2(matrix, puzzle)
    # print(utils.stateList)
    # print(utils.stateList1)
    # print(utils.stateList2)
    # print(matrix)
    # stateList.append(matrix)
    # backtracking
    # game = LightUpGame(matrix)
    # game.initGrid()
    # matrix = solve_puzzle_upgrade(matrix, puzzle, 7)
    # print(utils.stateList[0])
    # print(utils.stateList[1])
    # print(matrix)
    game.run(utils.stateList1, utils.stateList2)
