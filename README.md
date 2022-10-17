# 2048_Game_Bot

These are files for a program I wrote in the thick of the pandemic, in 2020.

I got bored, so I wrote a program to play the game 2048. 
If you've never seen this game before, check out [play2048.co]( https://play2048.co/ )

The program I wrote in 2020 opens up a chrome browser using the library
*selenium*, then it navigates to the website, and starts playing the game automatically. 

Here's a really well-shot video of the bot in action:

https://user-images.githubusercontent.com/48235053/196084178-315a8b72-3012-4de5-952e-b83e232c673f.MOV


However, PLEASE NOTE that the python code is... really awful.
Zero good software engineering practices.
* Comments? Nope
* DRY code? Nope
* test cases? Nope
* generally readable code? Absolutely not! 

The long-term goal here is to re-write the program logic in C++ to make it run faster, while still using python for interacting with the website. 
