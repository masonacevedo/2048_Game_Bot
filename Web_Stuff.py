from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

SITE_URL = "https://play2048.co"


def goToWebsite():
    
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(SITE_URL)

    return driver

def getGameStatus(driver):
    return driver.find_element_by_css_selector(".game-container p")

def getController(driver):
    return driver.find_element_by_css_selector('html')


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



def readScore(driver):
    scoreContainer = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]")
    if ("\n" in scoreContainer.text):
        indexOfNewline = scoreContainer.text.index("\n")
        return scoreContainer.text[0:indexOfNewline]
    else:
        return scoreContainer.text