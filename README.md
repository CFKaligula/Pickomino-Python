# Regenwormen-Python

This repository contains a `Python` implementation of the dice game "Pickomino" or "Regenwormen" in Dutch. 

## File Structure

The main file is called `pickomino.py`, running the `game()` function in this file will play the game. 
The `player_strategies.py` file contains strategies for the computer to play the game as well as the option for playing yourself.
The `globals.py` file contains some necessary global variables used by both `pickomino.py` and `player_strategies.py` such as the number of players. It also contains the `verbose` variable which if set to `True` will turn on all the `print()` statements.

`visualize.py` contains functions that make a nice visualization of dice by drawing some cubes with the value of the dice inside. `analyze.py` currently only contains a function to create a histogram of the results of the `analyze()` function in `pickomino.py`, which shows how much each player has won. Lastly, `player_strategy_test.py` generates random dice rolls and dice in hand and shows how a player strategy would react, an easy way to quickly analyze a player stategy's behavior.

## Playing yourself

Player strategies are set in the first few lines of the `game()` function in pickomino.py. You can play the game yourself by setting all player strategies to ` human_player` (and setting `verbose` to `True` in `globals.py`). You can set the number of players and their names in   `globals.py` with the respective variables.

## Other stuff

You can let the game be played as many times you want with the `analyze()`  function in pickomino.py, it will run as many games as set in `globals.py` and results will be placed in a file called `analyze.txt`.
