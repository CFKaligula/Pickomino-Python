import os
import sys
_DICE_OPTIONS = [1, 2, 3, 4, 5, "worm"]
_NUMBER_OF_DICE = 8
_NUMBER_OF_PLAYERS = 8
_NUMBER_OF_GAMES = 600

active_tiles = list(range(21, 37))
#player_tiles = [[] for _ in range(_NUMBER_OF_PLAYERS)]

player_name_dict = {
    0: "nul",
    1: "yksi",
    2: "zwei",
    3: "troi",
    4: "shi",
    5: "go",
    6: "zes",
    7: "septem",
    8: "hachi",
}

player_tiles = {player_name_dict[i]: [] for i in range(_NUMBER_OF_PLAYERS)}
_PLAYER_NAME_LIST = list(player_tiles.keys())


def reverse_dict(dict):
    return {v: k for k, v in dict.items()}


player_index_dict = reverse_dict(player_name_dict)


def sorted_dict(dict):
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}


def key_with_max_val(dict):
    v = list(dict.values())
    k = list(dict.keys())
    return k[v.index(max(v))]


def get_stealable_stones_dict(current_player_name):
    # makes a dictionary where the keys are the stealable tiles and values are the player who owns that tiles
    # stealable stones are the last taken stones
    player_name_list = list(player_tiles.keys())
    stealable_stones_dict = {}
    print(_PLAYER_NAME_LIST)
    for player_name in _PLAYER_NAME_LIST:
       print(player_name, current_player_name, player_name != current_player_name and len(player_tiles[player_name]) > 0)
       if player_name != current_player_name and len(player_tiles[player_name]) > 0:
            print(player_name, current_player_name, player_name != current_player_name and len(player_tiles[player_name]) > 0, player_tiles[player_name][-1])
     
            stealable_stones_dict[player_tiles[player_name][-1]] = player_name
        
          

    return stealable_stones_dict


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__
