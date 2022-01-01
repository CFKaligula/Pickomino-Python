from random import choices, seed, shuffle
import player_strategies
import globals
from time import sleep
import os
import visualize
import sys

#seed(69)


def sorted_dice(dice):
    return sorted(dice, key=lambda x: str(x), reverse=True)


def roll_dice(num_dice):
    return choices(globals._DICE_OPTIONS, k=num_dice)


def check_if_player_can_pick_dice(dice_roll, player_dice_in_hand):
    return not set(dice_roll).issubset(set(player_dice_in_hand))


def get_worm_num_from_tile_num(tile_num):
    return 1 + (tile_num - 21) // 4


def get_closest_lower_tile(num, active_tiles):
    last_tile = None
    result = None
    
    for tile in active_tiles:
        if tile > num:
            result = last_tile
            break
        if tile == num:
            result = tile
            break
        else:
            last_tile = tile
    else:
        #at the end of the loop, we have to check if the last active tile might be lower num
        if last_tile < num:
            print(num, active_tiles)
            result = last_tile
    return result


def put_tile_back_in_active_tiles(tile, active_tiles):
    for i in range(len(active_tiles)):
        if active_tiles[i] > tile:
            break
    active_tiles.insert(i, tile)
    return active_tiles


def decide_winner(round_num):
    print(f"The game is over after {round_num} rounds!")
    ranked_list = {}
    for player_name in globals._PLAYER_NAME_LIST:
        total_worm_amount = 0
        for tile in globals.player_tiles[player_name]:
            worm_number = get_worm_num_from_tile_num(tile)
            total_worm_amount += worm_number

        ranked_list[player_name] = total_worm_amount

    sorted_ranked_list = globals.sorted_dict(ranked_list)

    for player_name in sorted_ranked_list:
        print(f"Player {player_name}: {ranked_list[player_name]} worms, tiles: {globals.player_tiles[player_name]}")

    return list(sorted_ranked_list.keys())[0]


def game():
    # assign player strategies
    player_strategy_list = {globals.player_name_dict[i]: player_strategies.simple_player(globals.player_name_dict[i]) for i in range(globals._NUMBER_OF_PLAYERS)}
    '''
    player_strategy_list[0] = player_strategies.less_dumb_player(0)
    player_strategy_list[1] = player_strategies.thief(1)
    '''
    # randomly shuffle players so there is no first player advantage consistenly
    shuffled_player_list = list(globals.player_name_dict.values())[:globals._NUMBER_OF_PLAYERS]
    #shuffle(shuffled_player_list)
    shuffled_player_list = sorted(shuffled_player_list, reverse = True)


    round_num = 1

    while len(globals.active_tiles) > 0:
        #print("*"*20, "ROUND", round_num, "data:", "active tiles", globals.active_tiles, "player tiles", globals.player_tiles, "*"*20)
        round_num += 1

        for player_name in shuffled_player_list:
            print("*"*20,
                  "player turn:", player_name,
                  "player tiles", globals.player_tiles[player_name],
                  "active tiles", globals.active_tiles,
                  "*"*20,)

            # initialize turn variables
            player_turn_over = False
            player_stopped = False
            player_strategy = player_strategy_list[player_name]
            player_strategy.dice_in_hand = []
            rollable_dice_number = globals._NUMBER_OF_DICE  # number of dice to roll, dice in hand + rollable dice = number of dice

            # roll dice while possible
            while (not player_turn_over) and rollable_dice_number > 0:
                roll_stop_decision = player_strategy.decide_roll_or_stop()
                print("roll or stop decision:", roll_stop_decision)

                # player decides to roll
                if roll_stop_decision == "roll":
                    dice_roll = roll_dice(rollable_dice_number)

                    # visualize player's hand and rolled dice
                    print("dice in hand:")
                    visualize.visualize_dice(sorted_dice(player_strategy.dice_in_hand))
                    print("dice roll:")
                    visualize.visualize_dice(sorted_dice(dice_roll))

                    # check if it is possible for the player to pick any dice
                    dice_pick_check = check_if_player_can_pick_dice(dice_roll, player_strategy.dice_in_hand)
                    if dice_pick_check:
                        dice_pick_decision = player_strategy.decide_dice(dice_roll)
                        print("dice pick decision:", dice_pick_decision)

                        # if they pick 0, means there is no possible die to pick
                        if dice_pick_decision == 0:
                            player_turn_over = True
                            input("Dice pick decision is 0")
                        # extra check if a valid die is chosen
                        if dice_pick_decision not in dice_roll or dice_pick_decision in player_strategy.dice_in_hand:
                            raise Exception("INVALID DICE PICK DECISION")
                            input()

                        # add chosen die from roll to player's hand
                        if dice_pick_decision != 0:
                            for die in dice_roll:
                                if die == dice_pick_decision:
                                    player_strategy.dice_in_hand.append(die)
                                    rollable_dice_number -= 1
                    else:
                        print("Turn over, no dice to pick...",
                              "dice roll:", dice_roll,
                              "dice in hand:", player_strategy.dice_in_hand)
                        player_turn_over = True
                # player has chosen to stop
                else:
                    player_stopped = True
                    player_turn_over = True

                ''' after the player's turn is over '''
            if ("worm" in player_strategy.dice_in_hand) and player_stopped:
                player_dice_sum = player_strategy.dice_sum()

                # first check if tile can be stolen
                stealable_stones_dict = globals.get_stealable_stones_dict(player_name)
                if player_dice_sum in stealable_stones_dict:

                    chosen_tile = player_dice_sum
                    print("tile will be stolen", globals.player_tiles)
                    player_name_to_be_stolen_from = stealable_stones_dict[chosen_tile]
                    globals.player_tiles[player_name_to_be_stolen_from].remove(chosen_tile)
                    globals.player_tiles[player_name].append(chosen_tile)
                    print("tile is stolen", globals.player_tiles)
               

                # if the chosen tile is in the active tiles:
                # 1. remove it from active tiles
                # 2. add it to the player's tiles
                else:
                    chosen_tile = get_closest_lower_tile(player_dice_sum, globals.active_tiles)
                    if chosen_tile is not None:
                        print("tile taken from active:", chosen_tile, "active tiles:", globals.active_tiles)
                        globals.active_tiles.remove(chosen_tile)
                        globals.player_tiles[player_name].append(chosen_tile)
                        print("added tile", globals.player_tiles)
                    else:
                        #state that should be impossible to reach, just here for debug purpose
                        input("how did we get here")

                ''' player didn't stop in time or has no worm'''
            else:
                print("Not allowed to pick tile, no worm or not stopped:",
                      "dice in hand:", player_strategy.dice_in_hand,
                      "stopped:", player_stopped)
                chosen_tile = None  # set chosen tile at none for the print

                # when there is no valid dice to pick:
                # 1. remove the top stone from the tiles of the player
                # 2. return it to active tiles
                # 3. remove highest active tile (unless the highest tile was returned)
                if len(globals.player_tiles[player_name]) > 0:
                    returned_tile = globals.player_tiles[player_name][-1]
                    globals.player_tiles[player_name].remove(returned_tile)
                    globals.active_tiles = put_tile_back_in_active_tiles(returned_tile, globals.active_tiles)
                    if returned_tile != globals.active_tiles[-1]:
                        globals.active_tiles.pop(-1)
                else:
                    # if there is no stone to take, just remove highest active tile
                    globals.active_tiles.pop(-1)

            print(f"player {player_name} turn result:",
                  "dice in hand:",  player_strategy.dice_in_hand,
                  "dice sum:", player_strategy.dice_sum(),
                  "gotten tile:", chosen_tile,
                  "all player tiles:", globals.player_tiles)

            # stop the game if there are no active tiles left
            if len(globals.active_tiles) == 0:
                break

    return decide_winner(round_num)

def let_analyzed():
    globals.blockPrint()
    winner = game()

    folder_path = os.path.dirname(__file__)
    let_analysis_file_path = os.path.join(folder_path, "let_analysis.txt")
    with open(let_analysis_file_path, "a") as analysis_file:
        analysis_file.write(winner + "\n")

def analyze():
    winner_dict = {}
    for i in range(globals._NUMBER_OF_GAMES):

        globals.enablePrint()
        print("Game", i)
        globals.blockPrint()
        if i == 53:
            globals.enablePrint()
        if i > 54:
            quit()
        winner = game()
        # reset active tiles and player tiles for new game
        globals.active_tiles = list(range(21, 37))
        globals.player_tiles = {globals.player_name_dict[i]: [] for i in range(globals._NUMBER_OF_PLAYERS)}
        if winner in winner_dict:
            winner_dict[winner] += 1
        else:
            winner_dict[winner] = 1

    sorted_winner_dict = globals.sorted_dict(winner_dict)
    lines_to_write = []
    for player_name in sorted_winner_dict:
        lines_to_write.append(f"Player {player_name}: {sorted_winner_dict[player_name]} wins\n")

    folder_path = os.path.dirname(__file__)
    analysis_file_path = os.path.join(folder_path, "analysis.txt")
    with open(analysis_file_path, "w") as analysis_file:
        analysis_file.writelines(lines_to_write)
    print(sorted_winner_dict)


# game()
analyze()
#let_analyzed()
