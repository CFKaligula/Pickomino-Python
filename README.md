# Regenwormen-Python

This repository contains a Python implementation of the dice game "Pickomino" or "Regenwormen" in Dutch. 

## File Structure

The main file is called picomino.py, running the game() function in this file will play the game. 
The player_strategies.py file contains the CPU strategies for playing the game and also the option for playing as yourself, called human player.
The globals.py file contains some necessary global variables used by both picomino.py and player_strategies.py such as the number of players. It also contains the verbose variable which if set to True will turn on all the print statements.

## Playing yourself

player strategies are set in the first few lines of the game() function in picomino.py. You can play the game yourself by setting all player strategies to human_player (and setting verbose to True in globals.py).

## Other stuff

You can let the game be played as many times you want with the analyze() function in picomino.py.
