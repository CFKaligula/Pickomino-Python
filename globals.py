import os
import sys
from random import randint

verbose = False
_DICE_OPTIONS = [1, 2, 3, 4, 5, "worm"]
_NUMBER_OF_DICE = 8
_NUMBER_OF_PLAYERS = 2
_NUMBER_OF_GAMES = 1000

active_tiles = list(range(21, 37))

player_name_dict = {
    1: "een",
    2: "twee",
    3: "drie",
    4: "vier",
    5: "vijf",
    6: "zes",
    7: "zeven",
    8: "acht",
}

_PLAYER_NAME_LIST = list(player_name_dict.values())[:_NUMBER_OF_PLAYERS]
player_tiles = {_PLAYER_NAME_LIST[i]: [] for i in range(_NUMBER_OF_PLAYERS)}

def reverse_dict(dict):
    return {v: k for k, v in dict.items()}

player_index_dict = reverse_dict(player_name_dict)


def sorted_dict(dict):
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}


def key_with_max_val(dict):
    v = list(dict.values())
    max_val = max(v)
    max_index = 0
    #make sure we take a random key if there are multiple max elements
    for i in range(randint(1, v.count(max_val))):
        max_index = v.index(max_val, max_index)
    k = list(dict.keys())
    return k[max_index]


def get_stealable_stones_dict(current_player_name):
    # makes a dictionary where the keys are the stealable tiles and values are the player who owns that tiles
    # stealable stones are the last taken stones
    player_name_list = list(player_tiles.keys())
    stealable_stones_dict = {}
    
    for player_name in _PLAYER_NAME_LIST:
       if player_name != current_player_name and len(player_tiles[player_name]) > 0:
            if verbose: print(player_name, current_player_name, player_name != current_player_name and len(player_tiles[player_name]) > 0, player_tiles[player_name][-1])
   
            stealable_stones_dict[player_tiles[player_name][-1]] = player_name
        
          
    return stealable_stones_dict
