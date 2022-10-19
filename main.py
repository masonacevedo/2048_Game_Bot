
myBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
halfWeights = [0.5,0.5,0.5,0.5,
             0.5,0.5,0.5,0.5,
             0.5,0.5,0.5,0.5,
             0.5,0.5,0.5,0.5]
snakeWeights =  [[3**1, 3**2, 3**3, 3**4],
            [3**8, 3**7, 3**6, 3**5],
            [3**9, 3**10,3**11,3**12],
            [3**16,3**15,3**14,3**13]] 

def main(ply, weights):

    # The dream pseudocode:
    # 
    # navigate to website
    # while game isn't over:
    #   get the current board
    #   figure out the best move
    #   send the best move to the website. 

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://play2048.co")
    

    gameStatus = driver.find_element_by_css_selector(".game-container p")

    controller = driver.find_element_by_css_selector('html')

    while (gameStatus.text != "Game over!"):
        currentBoard = getTiles(driver)
        
        bestSequence = calculateBestSequenceSnake(currentBoard,ply, weights)
        
        if (bestSequence[0] == "Left"):
            controller.send_keys(Keys.LEFT)
        elif (bestSequence[0] == "Right"):
            controller.send_keys(Keys.RIGHT)
        elif (bestSequence[0] == "Up"):
            controller.send_keys(Keys.UP)
        else:
            controller.send_keys(Keys.DOWN)


