# o: white circle
# x: black circle
# -: not filled in

from timeit import default_timer
from queue import PriorityQueue
import psutil
import os


class BinairoSolver:
    def __init__(self, _matrix: list, _level: int):
        self.matrix = _matrix
        self.level = _level
        self.visited = []
        self.solved = False
        self.pq = PriorityQueue()
        self.pq.put((0, self.matrix, 0))

    # print a matrix
    def printMatrix(self, matrix, step=-1):
        if step == 0:
            print('-----Initial-----')
        elif step == -1:
            if matrix:
                print('------Result-----')
            else:
                print('=====Can\'t Solve=====')
                return
        else:
            print('-----Step '+str(step)+'-----')
        for row in matrix:
            for ele in row:
                print(ele, end='  ')
            print()

    # print all status of matrix from start to finish
    def printVisited(self):
        for i, v in enumerate(self.visited):
            self.printMatrix(v, i)

    # deep copy a matrix
    def copyMatrix(self, matrix):
        res = []
        for row in matrix:
            resRow = row.copy()
            res.append(resRow)
        return res

    # solve problem
    def solve(self):
        self.bestFirstSearch()

    def bestFirstSearch(self):
        while not self.pq.empty() and not self.solved:
            (_, matrix, step) = self.pq.get()
            if not matrix in self.visited:
                self.printMatrix(matrix, step)
                self.visited.append(matrix)
                newStates = self.findNewStates(matrix, step)
                if newStates is None:
                    continue
                elif newStates == []:
                    if self.checkGoal(matrix):
                        self.solved = True
                else:
                    for state in newStates:
                        t_matrix = self.copyMatrix(matrix)
                        t_matrix[state['r']][state['c']] = state['op']
                        self.pq.put((state['score'], t_matrix, state['step']))

    # check matrix is full fill
    def checkGoal(self, matrix):
        for row in matrix:
            if row.count('-') > 0:
                return False
        return True

    # find continue step
    # use funcH and funcG to generate states (A*)
    def findNewStates(self, matrix, step):
        newStates = []
        for r in range(self.level):
            for c in range(self.level):
                if matrix[r][c] != '-':
                    continue

                tryX = self.funcG(matrix, r, c, 'x')
                tryO = self.funcG(matrix, r, c, 'o')

                if tryX and tryO:
                    t_matrix = self.copyMatrix(matrix)

                    t_matrix[r][c] = 'x'
                    tryX = self.funcH(t_matrix, r, c, 'x')
                    newStates.append(
                        {'r': r, 'c': c, 'op': 'x', 'score': tryX, 'step': step+1})

                    t_matrix[r][c] = 'o'
                    tryO = self.funcH(t_matrix, r, c, 'o')
                    newStates.append(
                        {'r': r, 'c': c, 'op': 'o', 'score': tryO, 'step': step+1})

                elif tryX and not tryO:
                    return [{'r': r, 'c': c, 'op': 'x', 'score': 0, 'step': step+1}]
                elif tryO and not tryX:
                    return [{'r': r, 'c': c, 'op': 'o', 'score': 0, 'step': step+1}]
                else:
                    return None

        return newStates

    # function H
    def funcH(self, matrix, r, c, op):
        score = 8

        if matrix[r].count('-') == 1:
            c_idx = matrix[r].index('-')
            op_try = 'x' if op == 'o' else 'o'
            if self.funcG(matrix, r, c_idx, op_try):
                score -= 1

        if [matrix[i][c] for i in range(self.level)].count('-') == 1:
            r_idx = [matrix[i][c] for i in range(self.level)].index('-')
            op_try = 'x' if op == 'o' else 'o'
            if self.funcG(matrix, r_idx, c, op_try):
                score -= 1

        for i in range(self.level-2):
            if matrix[r][i] == matrix[r][i+1] and matrix[r][i+2] == '-' and (c == i or c == i+1):
                score -= 1
                break

        for i in range(1, self.level-1):
            if matrix[r][i] == matrix[r][i+1] and matrix[r][i-1] == '-' and (c == i or c == i+1):
                score -= 1
                break

        for i in range(self.level-2):
            if [matrix[i][c] for i in range(self.level)][i] == [matrix[i][c] for i in range(self.level)][i+1] and [matrix[i][c] for i in range(self.level)][i+2] == '-' and (c == i or c == i+1):
                score -= 1
                break

        for i in range(1, self.level-1):
            if [matrix[i][c] for i in range(self.level)][i] == [matrix[i][c] for i in range(self.level)][i+1] and [matrix[i][c] for i in range(self.level)][i-1] == '-' and (c == i or c == i+1):
                score -= 1
                break

        for i in range(self.level-2):
            if matrix[r][i] == matrix[r][i+2] and matrix[r][i+1] == '-' and (c == i or c == i+2):
                score -= 1
                break

        for i in range(self.level-2):
            if [matrix[i][c] for i in range(self.level)][i] == [matrix[i][c] for i in range(self.level)][i+2] and [matrix[i][c] for i in range(self.level)][i+1] == '-' and (c == i or c == i+2):
                score -= 1
                break

        return score

    # function G
    def funcG(self, matrix, r, c, op):
        def checkCount(lst: list):
            return True if lst.count(op) <= self.level/2 - 1 else False

        def checkTrio(lst: list, idx: int):
            if lst.count(op) <= 1:
                return True
            temp = lst.copy()
            temp[idx] = op
            for i in range(self.level-2):
                if temp[i] == temp[i+1] == temp[i+2] == op:
                    return False
            return True

        def checkSimular():
            tempMat = self.copyMatrix(matrix)
            tempMat[r][c] = op

            # True if not simular else False
            res = True

            # check simular rows
            if '-' not in tempMat[r] and tempMat.count(tempMat[r]) > 1:
                res = False

            # check simular column
            tempMat2 = [[tempMat[i][j]
                         for i in range(self.level)] for j in range(self.level)]
            if '-' not in tempMat[c] and tempMat2.count(tempMat2[c]) > 1:
                res = False
            return res

        def checkCreateTrio(lst: list, idx: int):
            if lst.count(op) < self.level/2 - 1:
                return True
            temp = lst.copy()
            temp[idx] = op
            for i in range(self.level-2):
                if temp[i] != op and temp[i+1] != op and temp[i+2] != op:
                    return False
            return True

        return checkCount(matrix[r]) and checkCount([matrix[i][c] for i in range(self.level)]) and checkTrio(matrix[r], c) and checkTrio([matrix[i][c] for i in range(self.level)], r) and checkSimular() and checkCreateTrio(matrix[r], c) and checkCreateTrio([matrix[i][c] for i in range(self.level)], r)


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


with open('testcase8x8.txt', 'r') as f:
    # f = open('testcase10x10.txt', 'r')
    inputData = f.read().split('\n')

    # get level
    inputLevel = len(inputData)

    # get problem
    inputMatrix = []
    for i in range(len(inputData)):
        inputRow = []
        for j in range(inputLevel):
            inputRow.append(inputData[i][j])
        inputMatrix.append(inputRow)

    start = default_timer()
    solver = BinairoSolver(inputMatrix, inputLevel)
    memBefore = process_memory()
    solver.solve()
    memAfter = process_memory()
    stop = default_timer()

    print('Usage Memory:', memAfter - memBefore, 'bytes')
    print('Time To Run: ', stop - start)