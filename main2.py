from lightup.backtracking import *
from lightup.hillclimbing import *
# puzzle = {
#     (0,1): 0,
#     (1,6): 3,
#     (2,2): 2,
#     (2,4): 2,
#     (4,2): 1,
#     (4,4): 5,
#     (5,0): 5,
#     (6,5): 0
# }
puzzle = {
    (0,2): 5,
    (0,4): 2,
    (1,4): 1,
    (2,0): 1,
    (2,1): 5,
    (2,6): 5,
    (3,3): 1,
    (4,0): 1,
    (4,5): 1,
    (4,6): 5,
    (5,2): 0,
    (6,2): 1,
    (6,4): 1
}
if __name__ == "__main__":
    matrix = init_matrix(puzzle, 7)

    # stack = []
    # backtracking(puzzle, matrix, 7, stack)
    # print(matrix)

    # matrix = solve_puzzle2(matrix, puzzle)
    # print(matrix)

    matrix = solve_puzzle_upgrade(matrix, puzzle, 7)
    print(matrix)
