from Moves import Move
import board

from Web_Stuff import getTiles, goToWebsite
import Web_Stuff as web


myBoard = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

MOVE_TO_KEY = {
    Move.UP: web.Keys.UP,
    Move.DOWN: web.Keys.DOWN,
    Move.RIGHT: web.Keys.RIGHT,
    Move.LEFT: web.Keys.LEFT
    }

def main(ply, weights):    
    """
    # Pseudocode:
    # go to website
    # while game isn't over:
    #   get current board from website
    #   figure out the best move
    #   send the best move to the website. 
    """
    

    driver = web.goToWebsite()
    controller = web.getController(driver)
    gameStatus = web.getStatus(driver)
    
    while (gameStatus.text != "Game over!"):
        
        currentBoard = getTiles(driver)
        bestMove = board.calculateBestMove(currentBoard, ply, weights)
        
        try:
            controller.send_keys(MOVE_TO_KEY[bestMove])
        except:
            raise("Invalid Move Sent to Controller")
        
        gameStatus = web.getStatus(driver)