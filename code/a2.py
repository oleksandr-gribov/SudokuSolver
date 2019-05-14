import csv
import itertools

class Board():

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self, filename):

        #initialize all of the variables
        self.n2 = 0
        self.n = 0
        self.spaces = 0
        self.board = None
        self.valsInRows = None
        self.valsInCols = None
        self.valsInBoxes = None
        self.unsolved = None

        #load the file and initialize the in-memory board with the data
        self.loadSudoku(filename)


    #loads the sudoku board from the given file
    def loadSudoku(self, filename):

        with open(filename) as csvFile:
            self.n = -1
            reader = csv.reader(csvFile)
            for row in reader:

                #Assign the n value and construct the approriately sized dependent data
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    if not self.n ** 2 == len(row):
                        raise Exception('Each row must have n^2 values! (See row 0)')
                    else:
                        self.n2 = len(row)
                        self.spaces = self.n ** 4
                        self.board = {}
                        self.valsInRows = [set() for _ in range(self.n2)]
                        self.valsInCols = [set() for _ in range(self.n2)]
                        self.valsInBoxes = [set() for _ in range(self.n2)]
                        self.unsolved = set(itertools.product(range(self.n2), range(self.n2)))

                #check if each row has the correct number of values
                else:
                    if len(row) != self.n2:
                        raise Exception('Each row mus\t have the same number of values. (See row ' + str(reader.line_num - 1) + ')')

                #add each value to the correct place in the board; record that the row, col, and box contains value
                for index, item in enumerate(row):
                    if not item == '':
                        self.board[(reader.line_num-1, index)] = int(item)
                        self.valsInRows[reader.line_num-1].add(int(item))
                        self.valsInCols[index].add(int(item))
                        self.valsInBoxes[self.rcToBox(reader.line_num-1, index)].add(int(item))
                        self.unsolved.remove((reader.line_num-1, index))


    ##########################################
    ####   Utility Functions
    ##########################################

    #converts a given row and column to its inner box number
    def rcToBox(self, row, col):
        return self.n * (row // self.n) + col // self.n

    #prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            #add row divider
            if r % self.n == 0 and not r == 0:
                if self.n2 > 9:
                    print("  " + "----" * self.n2)
                else:
                    print("  " + "---" * self.n2)

            row = ""

            for c in range(self.n2):

                if (r,c) in self.board:
                    val = self.board[(r,c)]
                else:
                    val = None

                #add column divider
                if c % self.n == 0 and not c == 0:
                    row += " | "
                else:
                    row += "  "

                #add value placeholder
                if self.n2 > 9:
                    if val is None: row += "__"
                    else: row += "%2i" % val
                else:
                    if val is None: row += "_"
                    else: row += str(val)
            print(row)


    ##########################################
    ####   Move Functions - YOUR IMPLEMENTATIONS GO HERE
    ##########################################

    # returns True if the space is empty and on the board,
    # and assigning val to it is not blocked by any constraints
    def isValidMove(self, space, val):
        if space not in self.board or space not in self.unsolved:
            return False
        else:
            row = self.valsInRows[space[0]]
            col = self.valsInCols[space[1]]
            box = self.valsInBoxes[self.rcToBox(space[0], space[1])]
            return (val not in row) and (val not in col) and (val not in box)
    # makes a move, records it in its row, col, and box, and removes the space from unsolved
    def makeMove(self, space, val):
        self.board[space] = val
        self.valsInRows[space[0]].add(val)
        self.valsInCols[space[1]].add(val)
        self.valsInBoxes[self.rcToBox(space[0], space[1])].add(val)
        self.unsolved.remove(space)

    # removes the move, its record in its row, col, and box, and adds the space back to unsolved
    def removeMove(self, space, val):
        self.board.pop(space, None)
        self.valsInRows[space[0]].remove(val)
        self.valsInCols[space[1]].remove(val)
        self.valsInBoxes[self.rcToBox(space[0], space[1])].remove(val)
        self.unsolved.add(space)

    # optional helper function for use by getMostConstrainedUnsolvedSpace
    def evaluateSpace(self, space):
        counter = 0
        counter += len(self.valsInCols[space[1]])
        counter += len(self.valsInRows[space[0]])
        counter += len(self.valsInBoxes[self.rcToBox(space[0], space[1])])
        return counter

    # gets the unsolved space with the most current constraints
    # returns None if unsolved is empty
    def getMostConstrainedUnsolvedSpace(self):
        if (len(self.unsolved)<=0):
           return None
        else:
            #leastPossible = self.unsolved[0]
            constraintsPerSpace = {}
            for j in self.unsolved:
                min = self.evaluateSpace(j)
                if self.evaluateSpace(j+1) < min:
                    min = self.evaluateSpace(j+1)
                # constraintsPerSpace[j] = counter
            # print(constraintsPerSpace)
            # maxConstrained =  max(constraintsPerSpace, key = lambda k: constraintsPerSpace.get(k))
            # print(maxConstrained)
            return min




class Solver:
    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self):
        pass

    ##########################################
    ####   Solver
    ##########################################

    # recursively selects the most constrained unsolved space and attempts
    # to assign a value to it

    # upon completion, it will leave the board in the solved state (or original
    # state if a solution does not exist)

    # returns True if a solution exists and False if one does not
    def solve(self, board):

        space = board.getMostConstrainedUnsolvedSpace()
        for val in range(1,10):
            if board.isValidMove(space,val):
                board.makeMove(space,val)
                if self.solve(board):
                    return True
                else:
                    board.removeMove(space,val)
        return False

if __name__ == "__main__":
    #change this to the input file that you'd like to test
    board = Board('tests/named-boards/dolphin.csv')
    s = Solver()
    s.solve(board)
    print(s.solve(board))
    board.print()
