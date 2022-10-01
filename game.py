from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import copy
import numpy as np
from webdriver_manager.chrome import ChromeDriverManager
import random
import matplotlib.pyplot as plt
import scipy.optimize
import statistics
import os

myBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
halfWeights = [0.5,0.5,0.5,0.5,
             0.5,0.5,0.5,0.5,
             0.5,0.5,0.5,0.5,
             0.5,0.5,0.5,0.5]
snakeWeights =  [[3**1, 3**2, 3**3, 3**4],
            [3**8, 3**7, 3**6, 3**5],
            [3**9, 3**10,3**11,3**12],
            [3**16,3**15,3**14,3**13]] 

def findAllOccurences(string, character):
    indexList = []
    adjustmentList = [0]

    copy = string
    while (copy.find(character) != -1):
        index = copy.find(character)
        indexList.append(index + adjustmentList[-1])
        adjustmentList.append(len(string) - len(copy[index+1::]))
        copy = copy[index+1::]
    
    return indexList

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


def getTiles(driver):
    tileContainer = driver.find_element_by_class_name("tile-container")
    tiles = tileContainer.get_attribute("outerHTML")
    beginBracketIndices = findAllOccurences(tiles, "<")
    endBracketIndices = findAllOccurences(tiles, ">")
    

    tileTable = [[0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]
    
    for index in range(0, len(beginBracketIndices)-1):
        if (index % 4 == 1):
            tileString = tiles[beginBracketIndices[index]:endBracketIndices[index]+1]
            columnIndex = int(tileString[tileString.find("p")+len("position-")])-1
            rowIndex = int(tileString[tileString.find("p") + len("position-1-")])-1

            beforeValueIndex = tileString.find("tile tile-")+len("tile tile-")
            afterValueIndex = tileString.find(" tile-position")
            tileValue = tileString[beforeValueIndex:afterValueIndex+1]
            
            tileTable[rowIndex][columnIndex] = int(tileValue)
    
    return tileTable

def deepMax(L):
    if ((len(L) == 1) and (type(L[0]) == int)):
        return L[0]
    elif ((len(L) != 1) and (type(L[0]) == int)):
        return max(L[0],deepMax(L[1:]))
    elif ((len(L) == 1)):
        return deepMax(L[0])
    else:
        return max(deepMax(L[0]), deepMax(L[1:]))


def arbitraryWeightsMetric(board, weights):
    total = 0
    for rowIndex in range(0, len(board)):
        for colIndex in range(0, len(board[0])):
            total += (weights[rowIndex][colIndex] * board[rowIndex][colIndex])
    return total

def snakeMetric(board):
    weights =  [[3**1, 3**2, 3**3, 3**4],
                [3**8, 3**7, 3**6, 3**5],
                [3**9, 3**10,3**11,3**12],
                [3**16,3**15,3**14,3**13]]    

    total = 0

    for rowIndex in range(0, len(board)):
        for colIndex in range(0, len(board[0])):
            total += (weights[rowIndex][colIndex] * board[rowIndex][colIndex])
    
    return total

def niceBoard(board):

    formattedString = ""
    longestNumLength = len(str(deepMax(board)))
    for outerIndex in range(0, len(board)):
        for innerIndex in range(0, len(board[outerIndex])):
            lengthToUse = longestNumLength - len(str(board[outerIndex][innerIndex]))
            lengthToUse += 2
            formattedString += (str(board[outerIndex][innerIndex]) + (lengthToUse * " ")) 
        formattedString += '\n'
    return formattedString

def addRandomTile(board):
    zeroCoordinates = []
    for outerIndex in range(0, len(board)):
        for innerIndex in range(0, len(board[0])):
            if board[outerIndex][innerIndex] == 0:
                zeroCoordinates.append((outerIndex, innerIndex))

    coordinatesToAddTo = random.choice(zeroCoordinates)
    addedValue = random.choice([2,4])
    board[coordinatesToAddTo[0]][coordinatesToAddTo[1]] = addedValue

def gameOver(board):
    for outerIndex in range(0, len(board)):
        for innerIndex in range(0, len(board)):
            if (board[outerIndex][innerIndex] == 0):
                return False
    moveList = ["Left", "Right", "Up", "Down"]
    for move in moveList:
        if (simulate(board, move) != "NO MOVE TO SIMULATE"):
            return False
    
    return True

def functionToMinimize(inputVector):
    weights = [[inputVector[0], inputVector[1], inputVector[2], inputVector[3]],
               [inputVector[4], inputVector[5], inputVector[6], inputVector[7]],
               [inputVector[8], inputVector[9], inputVector[10], inputVector[11]],
               [inputVector[12], inputVector[13], inputVector[14], inputVector[15]]]
    print("weights:",weights)
    return (1/(mainSimulator(weights, 1)))

def findBestWeights():
    initialGuess = [0, 1, 2, 3,
                    4,5,6,7,
                    8,9,10,11,
                    12,13,14,15]

    myBounds = ((0,15),(0,15),(0,15),(0,15),
                (0,15),(0,15),(0,15),(0,15),
                (0,15),(0,15),(0,15),(0,15),
                (0,15),(0,15),(0,15),(0,15))
    myAnswer = scipy.optimize.minimize(functionToMinimize, 
                                       x0 = initialGuess, 
                                       bounds = myBounds,
                                       options = {'maxiter':5, "disp":True})
    print(myAnswer)
    return myAnswer

def rawDataGenerator(weights, numDataPoints):
    dataList = []
    for index in range(0, numDataPoints):
        dataList.append(mainSimulator(weights,1))
    weightString = str(weights)
    fileName = "rawData" + weightString + ".txt"
    with open(fileName, 'a') as file_handle:
        for index in range(0, len(dataList)):
            file_handle.write(str(dataList[index]))
            file_handle.write("\n")

def graphComparison(n, weights):
    for index in range(100,n+100, 100):
        centralLimitTheorem(index, weights)

def centralLimitTheorem(numSamples, weights):
    weightString = str(weights)
    with open("rawData" + weightString + ".txt",'r') as file_handle:
        savelines = file_handle.readlines()
    
    listOfSampleMeans = []
    for index in range(0, len(savelines), numSamples):
        linesToUse = savelines[index:index+numSamples]
        sampleList = []
        for line in linesToUse:
            sampleList.append(int(line[0:-1]))
        #print(sampleList)
        listOfSampleMeans.append(np.average(sampleList))
    
    plt.hist(listOfSampleMeans)
    plt.show()


def averageScoreAsAFunctionOfWeights(weights, numRuns):
    averageList = []
    for index in range(0, numRuns):
        averageList.append(mainSimulator(weights, 1))
    ans = statistics.mean(averageList)
    print(ans)
    return ans

def zoomOut(weights, numAverages, numRuns):
    averageList = []
    for index in range(0, numAverages):
        averageList.append(averageScoreAsAFunctionOfWeights(weights, numRuns))
    plt.hist(averageList)
    plt.show()
    return np.average(averageList)

def zoomOutHistory(weights, numAverages, numRuns):
    averageList = []
    fileName = "previousRuns" + str(numRuns) + ".txt"
    if not(os.path.exists(fileName)):
        with open(fileName, 'w') as file_handle:
            pass

    with open(fileName, 'r') as file_handle:
        savelines = file_handle.readlines()
    
    for line in savelines:
        averageList.append(float(line[:-1]))

    for index in range(0, numAverages):
        averageList.append(averageScoreAsAFunctionOfWeights(weights, numRuns))
    with open(fileName, 'w') as file_handle:
        for index in range(0, len(averageList)):
            writeString = str(averageList[index])
            file_handle.write(writeString)
            file_handle.write("\n")

    plt.hist(averageList)
    plt.show()
    return np.average(averageList)

def mainSimulator(weights, ply):
    currentBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    addRandomTile(currentBoard)
    addRandomTile(currentBoard)
    while (not(gameOver(currentBoard))):
        
        
        # NEXT THING TO DO:
        # INCORPORATE THE ADDITION OF NEW TILES
        
        bestSequence = calculateBestSequenceSnake(currentBoard,ply, weights)
        counter = 1
        while (len(bestSequence) == 0):
            #print("Hey! This isn't useless!")
            bestSequence = calculateBestSequenceSnake(currentBoard, ply-counter, weights)
            counter -= 1
        #print(len(currentBoard))
        #print(len(currentBoard[0]))
        #print(len(currentBoard[1]))
        #print(len(currentBoard[2]))
        #print(len(currentBoard[3]))

        #print(bestSequence)
        #print(niceBoard(currentBoard))
        #print("currentBoard:\n", niceBoard(currentBoard))
        if (bestSequence[0] == "Left"):
            #print("LEFT")
            #input("Press Enter to continue...")
            currentBoard = simulate(currentBoard, "Left")
        elif (bestSequence[0] == "Right"):
            #print("RIGHT")
            #input("Press Enter to continue...")
            currentBoard = simulate(currentBoard, "Right")
        elif (bestSequence[0] == "Up"):
            #print("UP")
            #input("Press Enter to continue...")
            currentBoard = simulate(currentBoard, "Up")
        else:
            #print("DOWN")
            #input("Press Enter to continue...")
            currentBoard = simulate(currentBoard, "Down")
        #
        addRandomTile(currentBoard)
    #print("GAME OVER!\nTHIS WAS THE BOARD AT THE END")
    #print(niceBoard(currentBoard))
    #print("Another simulation has finished.")
    ans = deepMax(currentBoard)
    #print(ans)
    return ans

def readMoves():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://play2048.co")
    
    tileContainer = driver.find_element_by_class_name("tile-container")
    tiles = tileContainer.get_attribute("outerHTML")
    

def test():
    driver = webdriver.Chrome(ChromeDriverManager.install())

def main(ply, weights):
    
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # begin test
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    
    # driver = webdriver.Chrome(chrome_options=options)
    
    # driver = webdriver.Chrome("C:/Users/undoc/Desktop/Not_Sure_If_I_Can_Delete/chromedriver_win32/chromedriver.exe", chrome_options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://play2048.co")
    

    gameStatus = driver.find_element_by_css_selector(".game-container p")

    controller = driver.find_element_by_css_selector('html')

    while (gameStatus.text != "Game over!"):
        #time.sleep(0)
        #print("Immediately before getTiles()")
        currentBoard = getTiles(driver)
        
        # NEXT THING TO DO:
        # INCORPORATE THE ADDITION OF NEW TILES
        bestSequence = calculateBestSequenceSnake(currentBoard,ply, weights)
        
        #print("niceBoard(currentBoard)):\n")
        #print(niceBoard(currentBoard))
        #input("Press Enter to continue...")
        #print("currentBoard:\n", niceBoard(currentBoard))
        if (bestSequence[0] == "Left"):
            print("Left:\n", niceBoard(simulate(currentBoard, "Left")))
            controller.send_keys(Keys.LEFT)
        elif (bestSequence[0] == "Right"):
            print("Right:\n", niceBoard(simulate(currentBoard, "Right")))
            controller.send_keys(Keys.RIGHT)
        elif (bestSequence[0] == "Up"):
            print("Up:\n", niceBoard(simulate(currentBoard, "Up")))
            controller.send_keys(Keys.UP)
        else:
            print("Down:\n", niceBoard(simulate(currentBoard, "Down")))
            controller.send_keys(Keys.DOWN)
        #input("Press Enter to continue...")
        
        # print(calculateScore(board))


def readScore(driver):
    scoreContainer = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]")
    if ("\n" in scoreContainer.text):
        indexOfNewline = scoreContainer.text.index("\n")
        return scoreContainer.text[0:indexOfNewline]
    else:
        return scoreContainer.text
        

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
        
        #print("Results:", results)

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