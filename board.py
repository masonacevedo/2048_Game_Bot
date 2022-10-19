import copy
import random
import numpy as np

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
    

    def validMove(currentBoard, move):
        if (simulate(currentBoard, move) == "NO MOVE TO SIMULATE"):
            return False
        else:
            return True

    # Seems like we should probably get rid of this function...
    def deepMax(L):
        if ((len(L) == 1) and (type(L[0]) == int)):
            return L[0]
        elif ((len(L) != 1) and (type(L[0]) == int)):
            return max(L[0],deepMax(L[1:]))
        elif ((len(L) == 1)):
            return deepMax(L[0])
        else:
            return max(deepMax(L[0]), deepMax(L[1:]))



# This code is NOT DRY AT ALL. Gotta figure out 
# a way to make it DRY. 
def shiftDown(board):
    newBoard =  [[0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]
    for columnIndex in range(0,4):
        nonZeroValues = []
        for rowIndex in range(0,4):
            if (board[rowIndex][columnIndex] != 0):
                nonZeroValues.append(board[rowIndex][columnIndex])
        newCol = [0]*(4-len(nonZeroValues))
        for item in nonZeroValues:
            newCol.append(item)
        for rowIndex in range(0,4):
            newBoard[rowIndex][columnIndex] = newCol[rowIndex]
    return newBoard


def shiftUp(board):
    newBoard =  [[0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]

    for columnIndex in range(0,4):
        nonZeroValues = []
        for rowIndex in range(0,4):
            if (board[rowIndex][columnIndex] != 0):
                nonZeroValues.append(board[rowIndex][columnIndex])
        newCol = []
        for item in nonZeroValues:
            newCol.append(item)
        for index in range(0, 4-len(nonZeroValues)):
            newCol.append(0)
            
        for rowIndex in range(0,4):
            newBoard[rowIndex][columnIndex] = newCol[rowIndex]
    
    return newBoard


def shiftLeft(board):
    newBoard =  [[0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]

    for rowIndex in range(0,4):
        nonZeroValues = []
        for colIndex in range(0,4):
            if (board[rowIndex][colIndex] != 0):
                nonZeroValues.append(board[rowIndex][colIndex])
        newRow = []
        for item in nonZeroValues:
            newRow.append(item)
        for index in range(0, 4-len(nonZeroValues)):
            newRow.append(0)
            
        for colIndex in range(0,4):
            newBoard[rowIndex][colIndex] = newRow[colIndex]
    
    return newBoard


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




# Similar Dryness Problem Here

def simulate(board, move):

    if (move == "Down"):
        # move tiles down
        newBoard = shiftDown(board)
        # merge if necessary
        for columnIndex in range(0,4):
            doubledRows = []
            for rowIndex in range(1,4):
                if (newBoard[rowIndex-1][columnIndex] == newBoard[rowIndex][columnIndex] and newBoard[rowIndex][columnIndex] != 0):
                    doubledRows.append(rowIndex)
            for index in range(0,len(doubledRows)):
                newBoard[doubledRows[index]][columnIndex] = 2*newBoard[doubledRows[index]][columnIndex]
                newBoard[doubledRows[index]-1][columnIndex] = 0
        # after merging, move down again
        newBoard = shiftDown(newBoard)
    elif (move == "Up"):
        # move tiles down
        newBoard = shiftUp(board)
        # merge if necessary
        for columnIndex in range(0,4):
            doubledRows = []
            for rowIndex in range(0,3):
                if (newBoard[rowIndex][columnIndex] == newBoard[rowIndex+1][columnIndex] and newBoard[rowIndex][columnIndex] != 0):
                    doubledRows.append(rowIndex)
            for index in range(0,len(doubledRows)):
                newBoard[doubledRows[index]][columnIndex] = 2*newBoard[doubledRows[index]][columnIndex]
                newBoard[doubledRows[index]+1][columnIndex] = 0
        # after merging, move down again
        newBoard = shiftUp(newBoard)

    elif (move == "Left"):
        # move tiles down
        newBoard = shiftLeft(board)
        # merge if necessary
        for rowIndex in range(0,4):
            doubledCols = []
            for colIndex in range(0,3):
                if (newBoard[rowIndex][colIndex] == newBoard[rowIndex][colIndex+1] and newBoard[rowIndex][colIndex] != 0):
                    doubledCols.append(colIndex)
            for index in range(0,len(doubledCols)):
                newBoard[rowIndex][doubledCols[index]] = 2*newBoard[rowIndex][doubledCols[index]]
                newBoard[rowIndex][doubledCols[index]+1] = 0
        # after merging, move down again
        newBoard = shiftLeft(newBoard)

    else: # move == "Right"
        # move tiles down
        newBoard = shiftRight(board)
        # merge if necessary
        for rowIndex in range(0,4):
            doubledCols = []
            for colIndex in range(1,4):
                if (newBoard[rowIndex][colIndex-1] == newBoard[rowIndex][colIndex] and newBoard[rowIndex][colIndex] != 0):
                    doubledCols.append(colIndex)
            for index in range(0,len(doubledCols)):
                newBoard[rowIndex][doubledCols[index]] = 2*newBoard[rowIndex][doubledCols[index]]
                newBoard[rowIndex][doubledCols[index]-1] = 0
        # after merging, move down again
        newBoard = shiftRight(newBoard)
    
    if (newBoard == board):
        return "NO MOVE TO SIMULATE"
    else:
        return newBoard




# 


def addTiles(board):
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




def arbitraryWeightsMetric(board, weights):
    total = 0
    for rowIndex in range(0, len(board)):
        for colIndex in range(0, len(board[0])):
            total += (weights[rowIndex][colIndex] * board[rowIndex][colIndex])
    return total




def addRandomTile(board):
    zeroCoordinates = []
    for outerIndex in range(0, len(board)):
        for innerIndex in range(0, len(board[0])):
            if board[outerIndex][innerIndex] == 0:
                zeroCoordinates.append((outerIndex, innerIndex))

    coordinatesToAddTo = random.choice(zeroCoordinates)
    addedValue = random.choice([2,4])
    board[coordinatesToAddTo[0]][coordinatesToAddTo[1]] = addedValue





def calculateBestSequenceSnake(currentBoard, lookAhead, weights):
    if (lookAhead == 1):

        leftMove = simulate(currentBoard, "Left")
        rightMove = simulate(currentBoard, "Right")
        upMove = simulate(currentBoard, "Up")
        downMove = simulate(currentBoard, "Down")

        moves = [leftMove, rightMove, upMove, downMove]
        
        allowedMoves = ["NO"]*4
        for index in range(0, len(moves)):
            if (moves[index] != "NO MOVE TO SIMULATE"):
                allowedMoves[index] = moves[index]

        metrics = [-1]*4

        for index in range(0, len(allowedMoves)):
            if (allowedMoves[index] != "NO"):
                possibilities = addTiles(allowedMoves[index])
                possibleMetrics = [arbitraryWeightsMetric(board, weights) for board in possibilities]    
                metrics[index] = np.min(possibleMetrics)
            else:
                metrics[index] = -1
        
        

        if (metrics.index(max(metrics)) == 0):
            bestMove = "Left"
        elif (metrics.index(max(metrics)) == 1):
            bestMove = "Right"
        elif (metrics.index(max(metrics)) == 2):
            bestMove = "Up"
        else:
            bestMove = "Down"
        
        return [bestMove]
    else:
        if (validMove(currentBoard, "Left")):
            bestLeft = ["Left"] + calculateBestSequenceSnake(simulate(currentBoard, "Left"), lookAhead-1, weights)
        else:
            bestLeft = []
        
        if (validMove(currentBoard, "Right")):
            bestRight = ["Right"] + calculateBestSequenceSnake(simulate(currentBoard, "Right"), lookAhead-1, weights)
        else:
            bestRight = []
        
        if (validMove(currentBoard, "Up")):
            bestUp = ["Up"] + calculateBestSequenceSnake(simulate(currentBoard, "Up"), lookAhead-1, weights)
        else:
            bestUp = []

        if (validMove(currentBoard, "Down")):
            bestDown = ["Down"] + calculateBestSequenceSnake(simulate(currentBoard, "Down"), lookAhead-1, weights)
        else:
            bestDown = []
        
        
        leftResult = evaluateSequenceSnake(currentBoard, bestLeft, weights)
        rightResult = evaluateSequenceSnake(currentBoard, bestRight, weights)
        upResult = evaluateSequenceSnake(currentBoard, bestUp, weights)
        downResult = evaluateSequenceSnake(currentBoard, bestDown, weights)

        results = [leftResult, rightResult, upResult, downResult]
        
        bestIndex = results.index(max(results))
        if (bestIndex == 0):
            return bestLeft
        elif (bestIndex == 1):
            return bestRight
        elif (bestIndex == 2):
            return bestUp
        else:
            return bestDown


# inputs: a sequence of moves
# outputs: the average snake metric if you were to do those moves
def evaluateSequenceSnake(currentBoard, sequence, weights):
    if (len(sequence) == 0):
        return -1
    elif (validMove(currentBoard, sequence[0]) == False):
        return -1
    elif (len(sequence) == 1):
        
        move = simulate(currentBoard, sequence[0])
        
        possibilities = addTiles(move)
        possibleMetrics = [arbitraryWeightsMetric(board, weights) for board in possibilities]
        return np.min(possibleMetrics)
    else:
        move = simulate(currentBoard, sequence[0])
        possibilities = addTiles(move)

        averagesList = []
        for index in range(0, len(possibilities)):
            averagesList.append(evaluateSequenceSnake(possibilities[index], sequence[1:], weights))

        return np.min(averagesList)

def validMove(currentBoard, move):
    if (simulate(currentBoard, move) == "NO MOVE TO SIMULATE"):
        return False
    else:
        return True