# o: white circle
# x: black circle
# -: not filled in

from timeit import default_timer
import psutil
import os


class BinairoSolver:
    def __init__(self, _matrix: list, _level: int):
        self.matrix = _matrix
        self.level = _level
        self.log = []
    
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
                print(ele,end='  ')
            print()
    
    # print all status of matrix from start to finish
    def printLog(self):
        for i,v in enumerate(self.log[::-1]):
            self.printMatrix(v, i)
        self.printMatrix(self.matrix)

    # deep copy a matrix
    def copyMatrix(self, matrix):
        res = []
        for row in matrix:
            resRow = row.copy()
            res.append(resRow)
        return res

    # solve problem
    def solve(self):
        self.matrix = self.searchAndFill(self.matrix)

    # Deep-first Search
    def searchAndFill(self, matrix, r=0, c=0, step=0):
        self.printMatrix(matrix, step)

        if r==self.level:
            self.log.append(matrix)
            return matrix

        # cell have filled
        while matrix[r][c] != '-':
            r = r if c < self.level-1 else r+1
            if r==self.level:
                self.log.append(matrix)
                return matrix
            c = c+1 if c < self.level-1 else 0

        # copy matrix for searching
        t_matrix = self.copyMatrix(matrix)

        # cell have not filled yet
        # try 'x' value
        if self.tryFillInCell(t_matrix, r, c, 'x'):
            t_matrix[r][c] = 'x'
            res = self.searchAndFill(t_matrix, (r if c < self.level-1 else r+1), (c+1 if c < self.level-1 else 0), step+1)
            if res:
                self.log.append(matrix)
                return res
        
        # try 'o' value
        if self.tryFillInCell(t_matrix, r, c, 'o'):
            t_matrix[r][c] = 'o'
            res = self.searchAndFill(t_matrix, (r if c < self.level-1 else r+1), (c+1 if c < self.level-1 else 0), step+1)
            if res:
                self.log.append(matrix)
                return res
        
        return None

    def tryFillInCell(self, matrix, r, c, op):
        def checkCount(lst: list):
            return True if lst.count(op) <= self.level/2 - 1 else False

        def checkTrio(lst: list, idx: int):
            if lst.count(op)<=1: return True
            temp = lst.copy()
            temp[idx] = op
            for i in range(self.level-2):
                if temp[i]==temp[i+1]==temp[i+2]==op:
                    return False
            return True
        
        def checkSimular():
            tempMat = self.copyMatrix(matrix)
            tempMat[r][c] = op

            # True if not simular else False
            res = True

            # check simular rows
            if '-' not in tempMat[r] and tempMat.count(tempMat[r])>1:
                res = False
            
            # check simular column
            tempMat2 = [[tempMat[i][j] for i in range(self.level)] for j in range(self.level)]
            if '-' not in tempMat[c] and tempMat2.count(tempMat2[c])>1:
                res = False
            return res

        def checkCreateTrio(lst: list, idx: int):
            if lst.count(op)<self.level/2 - 1: return True
            temp = lst.copy()
            temp[idx] = op
            for i in range(self.level-2):
                if temp[i]!=op and temp[i+1]!=op and temp[i+2]!=op:
                    return False
            return True

        return checkCount(matrix[r]) and checkCount([matrix[i][c] for i in range(self.level)]) and checkTrio(matrix[r], c) and checkTrio([matrix[i][c] for i in range(self.level)], r) and checkSimular() and checkCreateTrio(matrix[r], c) and checkCreateTrio([matrix[i][c] for i in range(self.level)], r)
        

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


with open('testcase8x8.txt', 'r') as f:
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