import globals
import player_strategies
from picomino import roll_dice, let_player_roll
from random import randint, choices
import visualize
import os

_NUMBER_OF_DICE_ROLLS = 1000
player_strategy = player_strategies.smart_player("player")
for i in range(_NUMBER_OF_DICE_ROLLS):
    globals.active_tiles = list(range(21, 37))

    rollable_dice_number = randint(1, 8)
    player_strategy.dice_in_hand = choices(globals._DICE_OPTIONS, k=globals._NUMBER_OF_DICE - rollable_dice_number)

    roll_stop_decision = player_strategy.decide_roll_or_stop()
    if globals.verbose:
        print("roll or stop decision:", roll_stop_decision)

    # player decides to roll
    if roll_stop_decision == "roll":
        player_turn_over, rollable_dice_number = let_player_roll(rollable_dice_number, player_strategy)

    # player has chosen to stop
    else:
        if globals.verbose:
            print("Player decided to stop")
        if globals.verbose:
            print("dice in hand:")
            visualize.visualize_dice(player_strategy.dice_in_hand)

    if globals.verbose:
        input()
        os.system("cls||clear")
