from tent.utils.constraint import Problem, MinConflictsSolver, ExactSumConstraint, MinSumConstraint
import time

class mc:
    def __init__(self, board, row_clue, col_clue, size):
        self.state = board
        self.size = size
        self.row_clue = row_clue
        self.col_clue = col_clue
        self.block = [0] * (size * size)
        self.start_run_time = -1
        self.end_run_time = -1
        self.execute_time = -1

    def get_idx(self, i, j):
        return i * self.size + j
    
    def print_init(self):
        # print original puzzle
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 1:
                    print('1', end=' ')
                else:
                    print('0', end=' ')
            print()

    def min_conflict(self):
        self.start_run_time = time.time()
        problem = Problem(MinConflictsSolver(1000))
        problem.addVariables(range(self.size * self.size), [0, 1])
        block = self.block
        board = self.state

        # generate block constraint
        for i in range(self.size):
            for j in range(self.size):
                idx_ij = self.get_idx(i, j)

                # block tree cell
                if board[i][j] == 1:
                    block[idx_ij] = 1
                    problem.addConstraint(ExactSumConstraint(0), [idx_ij])
                    continue
                # block empty row or column
                if self.row_clue[i] == 0 or self.col_clue[j] == 0:
                    block[idx_ij] = 1
                    problem.addConstraint(ExactSumConstraint(0), [idx_ij])
                    continue

                # block cell has no tree around 
                cnt = 0
                for u in range(-1, 2):
                    for v in range(-1, 2):
                        if 0 <= i + u < self.size and 0 <= j + v < self.size and abs(u) + abs(v) <= 1:
                            idx = self.get_idx(i + u, j + v)
                            cnt += board[i + u][j + v]
                if cnt == 0:
                    block[idx_ij] = 1
                    problem.addConstraint(ExactSumConstraint(0), [idx_ij])

        # generate problem constraint
        for i in range(self.size):
            for j in range(self.size):
                # generate ajacent tree constraint
                if board[i][j] == 1:
                    list = []
                    for u in range(-1, 2):
                        for v in range(-1, 2):
                            if 0 <= i + u < self.size and 0 <= j + v < self.size and abs(u) + abs(v) <= 1:
                                idx = self.get_idx(i + u, j + v)
                                if block[idx] == 0:
                                    list.append(idx)
                    problem.addConstraint(MinSumConstraint(1), list)
                    continue

                # generate no adjacent tent constraint
                idx_ij = self.get_idx(i, j)
                if block[idx_ij] == 1:
                    continue
                list = [idx_ij]
                for u in range(-1, 2):
                    for v in range(-1, 2):
                        if 0 <= i + u < self.size and 0 <= j + v < self.size and abs(u) + abs(v) != 0:
                            idx = self.get_idx(i + u, j + v)
                            if block[idx] == 0:
                                list.append(idx)
                problem.addConstraint(lambda *args: args[0] == 0 or (sum(args) == 1 and args[0] == 1), list)

        # generate row constraint
        for i in range(self.size):
            list = [self.get_idx(i, j) for j in range(self.size)]
            problem.addConstraint(ExactSumConstraint(self.row_clue[i]), list)

        # generate column constraint
        for j in range(self.size):
            list = [self.get_idx(i, j) for i in range(self.size)]
            problem.addConstraint(ExactSumConstraint(self.col_clue[j]), list)

        # sometime the solver cannot find the solution because of the randomness
        for trial in range(100):
            # print('Trial', trial)
            start_time = time.time()
            solution = problem.getSolution()
            end_time = time.time()
            if solution is not None:
                self.execute_time = round(1000*(end_time - start_time),4)
                break

        return solution
        
    def run(self):
        solution = self.min_conflict()
        self.end_run_time = time.time()
        # print the solution
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 1:
                    print('1', end=' ')
                else:
                    print('2' if solution[self.get_idx(i, j)] else '0', end=' ')
            print()
        
    def runtime(self):
        all_execute_time = round(1000*(self.end_run_time - self.start_run_time),4)
        return self.execute_time, all_execute_time
