# 2048_Game_Bot

These are files for a program I wrote in the thick of the pandemic, in 2020.

I got bored, so I wrote a program to play the game 2048. 
If you've never seen this game before, check out [play2048.co]( https://play2048.co/ )

The program opens up a chrome browser using the library
*selenium*, then it navigates to the website, and starts playing the game automatically. 

Here's a really well-shot video of the bot in action:

https://user-images.githubusercontent.com/48235053/196084178-315a8b72-3012-4de5-952e-b83e232c673f.MOV


Here is a rough idea of how the bot works:
1. It uses Python's *Selenium* library to navigate to the game website, and read the current state of the board.
2. It uses an algorithm I've designed to determine the best move.
3. It sends the best move to the website, reads the current state of the board, and goes back to step 2.

Great! But how does step 2 work? That's the meat of this project. 
Firstly, the code uses a max/min approach to determining the best move. That is, 
among the four moves (LEFT/RIGHT/UP/DOWN), the algorithm considers the worst-case scenario associated with each move, and then returns the move with the best worst-case scenario. 

Additionally, it's worth noting that the bot accepts a *ply* value. Informally, this is how far ahead into the future the bot looks. For a ply value of 2, the bot generates all possibilites sequences of 2 moves, simulates them, and then returns the worst-case scenario. For a ply value of 3, the bot generates all possible sequences of 3 moves, and returns the worst-case scenario of all those. Note that this means the  ply has an exponential relationship with the number of possibilities the bot has to consider. 

Finally, how exactly does the bot evaluate "how good" the board is? Phrased another way, how does the bot look at all the possibilities and determine which is the worst? Well, I've defined a scoring function that assigns boards points. The scoring function awards the highest values to boards with the largest tile in the bottom left corner, the 2nd-largest tile immediately to it's right, the 3rd-largest tile immediately to it's right, the 4th-largest tile in the bottom-right corner, and the 5th largest tile immediately *above it*. Here's a little drawing that demonstrates what the scoring function looks for:



However, PLEASE NOTE that the python code is currently in development!
It doesn't work as-is, because the previous
version needed LOTS of refactoring. I will add test-cases and a makefile
soon! 

The long-term goal here is to re-write the program logic in C++ to make it run faster, while still using python for interacting with the website. 