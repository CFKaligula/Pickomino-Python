_DICE_OPTIONS = [1, 2, 3, 4, 5, "worm"]
_NUMBER_OF_DICE = 8
_NUMBER_OF_PLAYERS = 3
_NUMBER_OF_GAMES = 3000

active_tiles = list(range(21, 37))
player_tiles = [[] for _ in range(_NUMBER_OF_PLAYERS)]

player_name_dict = {
    0: "zero",
    1: "the one",
    2: "snake",
    3: "free",
    4: "fury",
    5: "goku",
    6: "sechs",
    7: "nana",
    8: "hachi",
}

def sorted_dict(dict):
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}


def key_with_max_val(dict):
    v = list(dict.values())
    k = list(dict.keys())
    return k[v.index(max(v))]


def get_stealable_stones_dict(current_player):
    stealable_stones_dict = {}
    for player in range(len(player_tiles)):
        if player == current_player:
            continue
        else:
            if len(player_tiles[player]) > 0:
                stealable_stones_dict[player_tiles[player][-1]] = player

    return stealable_stones_dict


import sys, os


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__
    
    
blockPrint()