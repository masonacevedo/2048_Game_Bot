import copy
import random
from Moves import Move


# How do we want to deal with the weights? 
# Is this an object of type board?
# On the one hand, it is a grid of 16 values,
# similar to a board. On the other hand, 
# it does not -- and should not -- 
# support the same functionality: finding the 
# best move, simulating an arbitrary sequence of 
# moves, etc... 
SNAKE_WEIGHTS =  [[3**1, 3**2, 3**3, 3**4],
            [3**8, 3**7, 3**6, 3**5],
            [3**9, 3**10,3**11,3**12],
            [3**16,3**15,3**14,3**13]]

PRECOMPUTED_SEQUENCES = {
1: [[Move.UP], [Move.RIGHT], [Move.DOWN], [Move.LEFT]],

2: [[Move.UP, Move.UP],
 [Move.UP, Move.RIGHT],
 [Move.UP, Move.DOWN],
 [Move.UP, Move.LEFT],
 [Move.RIGHT, Move.UP],
 [Move.RIGHT, Move.RIGHT],
 [Move.RIGHT, Move.DOWN],
 [Move.RIGHT, Move.LEFT],
 [Move.DOWN, Move.UP],
 [Move.DOWN, Move.RIGHT],
 [Move.DOWN, Move.DOWN],
 [Move.DOWN, Move.LEFT],
 [Move.LEFT, Move.UP],
 [Move.LEFT, Move.RIGHT],
 [Move.LEFT, Move.DOWN],
 [Move.LEFT, Move.LEFT]],


 3: [[Move.UP, Move.UP, Move.UP],
 [Move.UP, Move.UP, Move.RIGHT],
 [Move.UP, Move.UP, Move.DOWN],
 [Move.UP, Move.UP, Move.LEFT],
 [Move.UP, Move.RIGHT, Move.UP],
 [Move.UP, Move.RIGHT, Move.RIGHT],
 [Move.UP, Move.RIGHT, Move.DOWN],
 [Move.UP, Move.RIGHT, Move.LEFT],
 [Move.UP, Move.DOWN, Move.UP],
 [Move.UP, Move.DOWN, Move.RIGHT],
 [Move.UP, Move.DOWN, Move.DOWN],
 [Move.UP, Move.DOWN, Move.LEFT],
 [Move.UP, Move.LEFT, Move.UP],
 [Move.UP, Move.LEFT, Move.RIGHT],
 [Move.UP, Move.LEFT, Move.DOWN],
 [Move.UP, Move.LEFT, Move.LEFT],
 [Move.RIGHT, Move.UP, Move.UP],
 [Move.RIGHT, Move.UP, Move.RIGHT],
 [Move.RIGHT, Move.UP, Move.DOWN],
 [Move.RIGHT, Move.UP, Move.LEFT],
 [Move.RIGHT, Move.RIGHT, Move.UP],
 [Move.RIGHT, Move.RIGHT, Move.RIGHT],
 [Move.RIGHT, Move.RIGHT, Move.DOWN],
 [Move.RIGHT, Move.RIGHT, Move.LEFT],
 [Move.RIGHT, Move.DOWN, Move.UP],
 [Move.RIGHT, Move.DOWN, Move.RIGHT],
 [Move.RIGHT, Move.DOWN, Move.DOWN],
 [Move.RIGHT, Move.DOWN, Move.LEFT],
 [Move.RIGHT, Move.LEFT, Move.UP],
 [Move.RIGHT, Move.LEFT, Move.RIGHT],
 [Move.RIGHT, Move.LEFT, Move.DOWN],
 [Move.RIGHT, Move.LEFT, Move.LEFT],
 [Move.DOWN, Move.UP, Move.UP],
 [Move.DOWN, Move.UP, Move.RIGHT],
 [Move.DOWN, Move.UP, Move.DOWN],
 [Move.DOWN, Move.UP, Move.LEFT],
 [Move.DOWN, Move.RIGHT, Move.UP],
 [Move.DOWN, Move.RIGHT, Move.RIGHT],
 [Move.DOWN, Move.RIGHT, Move.DOWN],
 [Move.DOWN, Move.RIGHT, Move.LEFT],
 [Move.DOWN, Move.DOWN, Move.UP],
 [Move.DOWN, Move.DOWN, Move.RIGHT],
 [Move.DOWN, Move.DOWN, Move.DOWN],
 [Move.DOWN, Move.DOWN, Move.LEFT],
 [Move.DOWN, Move.LEFT, Move.UP],
 [Move.DOWN, Move.LEFT, Move.RIGHT],
 [Move.DOWN, Move.LEFT, Move.DOWN],
 [Move.DOWN, Move.LEFT, Move.LEFT],
 [Move.LEFT, Move.UP, Move.UP],
 [Move.LEFT, Move.UP, Move.RIGHT],
 [Move.LEFT, Move.UP, Move.DOWN],
 [Move.LEFT, Move.UP, Move.LEFT],
 [Move.LEFT, Move.RIGHT, Move.UP],
 [Move.LEFT, Move.RIGHT, Move.RIGHT],
 [Move.LEFT, Move.RIGHT, Move.DOWN],
 [Move.LEFT, Move.RIGHT, Move.LEFT],
 [Move.LEFT, Move.DOWN, Move.UP],
 [Move.LEFT, Move.DOWN, Move.RIGHT],
 [Move.LEFT, Move.DOWN, Move.DOWN],
 [Move.LEFT, Move.DOWN, Move.LEFT],
 [Move.LEFT, Move.LEFT, Move.UP],
 [Move.LEFT, Move.LEFT, Move.RIGHT],
 [Move.LEFT, Move.LEFT, Move.DOWN],
 [Move.LEFT, Move.LEFT, Move.LEFT]]}

class Board:
    
    def __init__(self):
        self.tiles = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
            ]

    def __str__(self):

        formattedString = ""
        longestNumLength = len(str(deepMax(self.tiles)))
        for outerIndex in range(0, len(self.tiles)):
            for innerIndex in range(0, len(self.tiles[outerIndex])):
                lengthToUse = longestNumLength - len(str(self.tiles[outerIndex][innerIndex]))
                lengthToUse += 2
                formattedString += (str(self.tiles[outerIndex][innerIndex]) + (lengthToUse * " ")) 
            formattedString += '\n'

        return formattedString
    
def calculateBestMove(currentBoard, ply):
    """
    Given the current state of the game, and a "ply"
    value, which is how many steps into the future
    to look ahead, this function returns the best 
    move. 

    Specifically, we define the "best" move as a 
    max-min of all the possibilities:
    If we look at the worst-case scenario for
    moving up, down, left, or right, which of 
    these moves has the best worst-case scenario?
    That's the one we return. 
    """
    # First, get all possible sequences of 
    # 4 moves. (There are 4^ply of these)
    sequences = getSequences(ply)

    worstOutcomes = []
    for sequence in sequences:
        firstMove = sequence[0]
        if validMove(firstMove):
            possibleOutcomes = simulateSequence(currentBoard, sequence)
            scores = [evaluateBoard(outcome) for outcome in possibleOutcomes]
            worstOutcomes.append((min(scores), firstMove))
    score, move = min(worstOutcomes)

    return move

def simulateSequence(board, sequence):
    """
    Given a sequence of moves to simulate,
    and a board, this function returns
    all the possible outcomes after
    simulating every one of those moves. 
    """
    if len(sequence) == 1:
        newBoard = board.shift(move)        
        possibleBoards = addTiles(newBoard)
        return possibleBoards
    else:
        firstMove = sequence[0]
        restOfSequence = sequence[1:]
        newBoard = shiftBoard(firstMove)
        possibleBoards = addTiles(newBoard)
        # now, for each of the possible boards, 
        # we need to simulate the next move
        # in the sequence... 
        ans = []
        for board in possibleBoards:
            ans = ans + simulateSequence(board, restOfSequence)

        return ans

def getSequences(n):
    """
    Given a positive integer n,
    this function returns all 
    the possible sequences of n
    moves.

    Note that the vast majority of the time,
    we're expecting n=1,2, or 3. 4 and
    above is rare enough that we 
    won't bother. 
    """

    if n in PRECOMPUTED_SEQUENCES:
        return PRECOMPUTED_SEQUENCES[n]
    else:
        shorterSequences = getSequences(n-1)
        ans = []
        for sequence in shorterSequences:    
            for move in Move:
                ans.append(sequence + [move])
        return ans

def addRandomTile(self):
    """ Adds a 2 or 4 to the board in a random, empty tile. """
    
    # before adding a random tile,
    # we have to figure out which
    # tiles are empty.
    emptyCoordinates = []
    for outerIndex in range(0, len(self.tiles)):
        for innerIndex in range(0, len(self.tiles[0])):
            if self.tiles[outerIndex][innerIndex] == 0:
                emptyCoordinates.append((outerIndex, innerIndex))

    row, col = random.choice(emptyCoordinates)
    addedValue = random.choice([2,4])
    self.tiles[row][col] = addedValue

def validMove(self, move):
    if (self.simulate(move) == "NO MOVE TO SIMULATE"):
        return False
    else:
        return True


def shift(board, direction):
    """
    Inputs: 
        A board, and the direction to shift it in
    Outputs: 
        The board after the shift 
        in the specified direction. 
    """

    move = moveList[0]
    
    if move == Move.DOWN:
        rotateCCW(board)
    elif move == Move.UP:
        rotateCW(board)
    elif move == Move.LEFT:
        rotateCCW(board)
        rotateCCW(board)
    elif move == Move.RIGHT:
        pass
    else:
        raise("Board has been asked to simulate an invalid move.")

    shiftRight(board)
    
    if move == Move.DOWN:
        rotateCW(board)
    elif move == Move.UP:
        rotateCCW(board)
    elif move == Move.LEFT:
        rotateCW(board)
        rotateCW(BOARD)
    elif move == Move.RIGHT:
        pass
    else:
        raise("Board has been asked to simulate an invalid move.")

    return

# This code is NOT DRY AT ALL. Gotta figure out 
# a way to make it DRY. 
def shiftRight(board):
    newBoard =  [[0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]

    for rowIndex in range(0,4):
        nonZeroValues = []
        for colIndex in range(0,4):
            if (board[rowIndex][colIndex] != 0):
                nonZeroValues.append(board[rowIndex][colIndex])
        
        newRow = [0]*(4-len(nonZeroValues))
        for item in nonZeroValues:
            newRow.append(item)
        for colIndex in range(0,4):
            newBoard[rowIndex][colIndex] = newRow[colIndex]
    
    return newBoard

def rotateCW(board):
    pass

def rotateCCW(board):
    rotateCW(board)
    rotateCW(board)
    rotateCW(board)
    


def addTiles(self):
    # returns a list containing all the possibilities
    # of where a new square can be added and what that square might be
    possibilitiesList = []
    possibilitiesBoard = copy.deepcopy(board)
    for rowIndex in range(0, len(board)):
        for colIndex in range(0, len(board[0])):
            if (board[rowIndex][colIndex] == 0):
                possibilitiesBoard[rowIndex][colIndex] = 2
                addedBoard = copy.deepcopy(possibilitiesBoard)
                possibilitiesList.append(addedBoard)

                possibilitiesBoard[rowIndex][colIndex] = 4
                addedBoard = copy.deepcopy(possibilitiesBoard)
                possibilitiesList.append(addedBoard)

                possibilitiesBoard[rowIndex][colIndex] = 0 

    return possibilitiesList




def evaluateBoard(board):
    total = 0
    for rowIndex in range(0, len(board)):
        for colIndex in range(0, len(board[0])):
            total += (SNAKE_WEIGHTS[rowIndex][colIndex] * board[rowIndex][colIndex])
    return total



# # inputs: a sequence of moves
# # outputs: the average snake metric if you were to do those moves
# def evaluateSequenceSnake(currentBoard, sequence, weights):
#     if (len(sequence) == 0):
#         return -1
#     elif (validMove(currentBoard, sequence[0]) == False):
#         return -1
#     elif (len(sequence) == 1):
        
#         move = simulate(currentBoard, sequence[0])
        
#         possibilities = addTiles(move)
#         possibleMetrics = [arbitraryWeightsMetric(board, weights) for board in possibilities]
#         return np.min(possibleMetrics)
#     else:
#         move = simulate(currentBoard, sequence[0])
#         possibilities = addTiles(move)

#         averagesList = []
#         for index in range(0, len(possibilities)):
#             averagesList.append(evaluateSequenceSnake(possibilities[index], sequence[1:], weights))

#         return np.min(averagesList)

def validMove(currentBoard, move):
    if (simulate(currentBoard, move) == "NO MOVE TO SIMULATE"):
        return False
    else:
        return True