from random import choices, seed
import player_strategies
import globals
from time import sleep
import os
import visualize
import sys
# seed(1)


def sorted_dice(dice):
    return sorted(dice, key=lambda x: str(x), reverse=True)


def roll_dice(num_dice):
    return choices(globals._DICE_OPTIONS, k=num_dice)


def check_if_player_can_pick_dice(rolled_dice, player_picked_dice):
    rolled_dice_options = set(rolled_dice)
    player_picked_dice_options = set(player_picked_dice)
    result = False
    for rolled_dice_option in rolled_dice_options:
        if rolled_dice_option not in player_picked_dice_options:
            result = True
            break
    return result


def get_worm_num_from_tile_num(tile_num):
    return 1 + (tile_num - 21) // 4


def get_closest_lower_tile(num, active_tiles):
    last_tile = 0
    result = 0
    for tile in active_tiles:
        if tile > num:
            result = last_tile
            break
        if tile == num:
            result = tile
            break
        else:
            last_tile = tile
    return result


def put_tile_back_in_active_tiles(tile, active_tiles):
    for i in range(len(active_tiles)):
        if active_tiles[i] > tile:
            break
    active_tiles.insert(i, tile)
    return active_tiles


def decide_winner(round_num):
    # decide winner
    print(f"The game is over after {round_num} rounds!")
    ranked_list = {}
    player_worm_numbers = [0 for _ in range(globals._NUMBER_OF_PLAYERS)]
    for player in range(globals._NUMBER_OF_PLAYERS):
        total_worm_amount = 0
        for tile in globals.player_tiles[player]:
            worm_number = get_worm_num_from_tile_num(tile)
            total_worm_amount += worm_number

        ranked_list[player] = total_worm_amount

    sorted_ranked_list = globals.sorted_dict(ranked_list)

    for player in sorted_ranked_list:
        print(f"Player {player}: {ranked_list[player]} worms, tiles: {globals.player_tiles[player]}")

    return list(sorted_ranked_list.keys())[0]


def game():
    # initialize the players
    player_strategy_list = [player_strategies.simple_player(i) for i in range(globals._NUMBER_OF_PLAYERS)]
    player_strategy_list[5] = player_strategies.less_dumb_player(5)

    round_num = 1

    while len(globals.active_tiles) > 0:
        #print("*"*20, "ROUND", round_num, "data:", "active tiles", globals.active_tiles, "player tiles", globals.player_tiles, "*"*20)
        round_num += 1
        for player in range(globals._NUMBER_OF_PLAYERS):
            print("*"*20,
                  "player turn:", player,
                  "player tiles", globals.player_tiles[player],
                  "active tiles", globals.active_tiles,
                  "*"*20,)

            # initialize turn variables
            player_turn_over = False
            player_stopped = False
            player_strategy = player_strategy_list[player]
            player_strategy.dice_in_hand = []
            player_strategy.rollable_dice_number = globals._NUMBER_OF_DICE

            # roll dice while possible
            while (not player_turn_over) and player_strategy.rollable_dice_number > 0:
                roll_stop_decision = player_strategy.decide_roll_or_stop()
                print("roll or stop decision:", roll_stop_decision)

                if roll_stop_decision == "roll":
                    dice_roll = sorted_dice(roll_dice(player_strategy.rollable_dice_number))
                    print("dice in hand:")
                    visualize.visualize_dice(sorted_dice(player_strategy.dice_in_hand))
                    print("dice roll:")
                    visualize.visualize_dice(dice_roll)
                    # check if it is possible for the player to pick any dice
                    dice_pick_check = check_if_player_can_pick_dice(dice_roll, player_strategy.dice_in_hand)
                    if dice_pick_check:
                        dice_pick_decision = player_strategy.decide_dice(dice_roll)
                        print("dice pick decision:", dice_pick_decision)

                        if dice_pick_decision == 0:
                            player_turn_over = True

                        if dice_pick_decision not in dice_roll or dice_pick_decision in player_strategy.dice_in_hand or dice_pick_decision == 0:
                            raise Exception("INVALID DICE PICK DECISION")

                        # add die from roll to player's hand
                        for die in dice_roll:
                            if die == dice_pick_decision:
                                player_strategy.dice_in_hand.append(die)
                                player_strategy.rollable_dice_number -= 1
                    else:
                        print("Turn over, no dice to pick...",
                              "dice roll:", dice_roll,
                              "dice in hand:", player_strategy.dice_in_hand)
                        player_turn_over = True
                # player has chosen to stop
                else:
                    player_stopped = True
                    player_turn_over = True

            # after the player's turn is over
            player_dice_sum = player_strategy.dice_sum()
            if "worm" in player_strategy.dice_in_hand:
                chosen_tile = get_closest_lower_tile(player_dice_sum, globals.active_tiles)
                # check if tile can be stolen

                stealable_stones_dict = globals.get_stealable_stones_dict(player)
                if player_dice_sum in stealable_stones_dict:
                    chosen_tile = player_dice_sum
            else:
                print("No worm in dice in hand:", player_strategy.dice_in_hand)
                chosen_tile = 0

            print("players turn result:",
                  "dice in hand:",  player_strategy.dice_in_hand,
                  "dice sum:", player_dice_sum,
                  "gotten tile:", chosen_tile)

            # when there is no valid dice to pick:
            # 1. remove the top stone from the tiles of the player
            # 2. return it to active tiles
            # 3. remove highest active tile (unless the highest tile was returned)
            if chosen_tile == 0:
                if len(globals.player_tiles[player]) > 0:
                    returned_tile = globals.player_tiles[player][-1]
                    globals.player_tiles[player].pop(-1)
                    globals.active_tiles = put_tile_back_in_active_tiles(returned_tile, globals.active_tiles)
                    if returned_tile != globals.active_tiles[-1]:
                        globals.active_tiles.pop(-1)

                else:
                    # if there is no stone to take, just remove highest active tile
                    globals.active_tiles.pop(-1)

            # if there *is* a valid dice AND player decided to stop:
            # 1. remove it from active tiles
            # 2. add it to the player's tiles
            elif player_stopped:
                if chosen_tile in globals.active_tiles:
                    print("tile taken from active:", chosen_tile, "active tiles:", globals.active_tiles)
                    globals.active_tiles.remove(chosen_tile)
                    globals.player_tiles[player].append(chosen_tile)
                    print("added tile", globals.player_tiles)
                else:  # the tile will be stolen
                    print("tile will be stolen", globals.player_tiles)
                    player_to_be_stolen = stealable_stones_dict[chosen_tile]
                    globals.player_tiles[player_to_be_stolen].pop(-1)
                    globals.player_tiles[player].append(chosen_tile)
                    print("tile is stolen", globals.player_tiles)

            # stop the game if there are no active tiles left
            if len(globals.active_tiles) == 0:
                break
            # input()
            print("all player tiles", globals.player_tiles)

    return decide_winner(round_num)


def analyze():
    winner_dict = {}
    for i in range(10000):
        winner = game()
        globals.active_tiles = list(range(21, 37))
        globals.player_tiles = [[] for _ in range(globals._NUMBER_OF_PLAYERS)]
        if winner in winner_dict:
            winner_dict[winner] += 1
        else:
            winner_dict[winner] = 1

    sorted_winner_dict = globals.sorted_dict(winner_dict)
    print(sorted_winner_dict)


# game()
analyze()
