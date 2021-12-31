from random import choices, seed
import player_strategies
import globals
from time import sleep
import os
seed(0)


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
        if tile == num:
            result = tile
        else:
            last_tile = tile
    return result


def put_tile_back_in_active_tiles(tile, active_tiles):
    for i in range(len(active_tiles)):
        if active_tiles[i] > tile:
            break
    active_tiles.insert(i, tile)
    return active_tiles


def game():
    # initialize the players
    player_strategy_list = [player_strategies.simple_player() for _ in range(globals._NUMBER_OF_PLAYERS)]
    print("starting")
    round_num = 1

    while len(globals.active_tiles) > 0:
        print("ROUND", round_num, "data:", globals.active_tiles, globals.player_tiles)
        input()
        os.sytem("cls||clear")
        round_num += 1
        for player in range(globals._NUMBER_OF_PLAYERS):
            print("player turn:", player,
                  "player tiles", globals.player_tiles[player],
                  "active tiles", globals.active_tiles)

            # initialize turn variables
            player_turn_over = False
            player_strategy = player_strategy_list[player]
            player_strategy.dice_in_hand = []
            player_strategy.rollable_dice_number = globals._NUMBER_OF_DICE

            # roll dice while possible
            while (not player_turn_over) and player_strategy.rollable_dice_number > 0:
                roll_stop_decision = player_strategy.decide_roll_or_stop()
                print("roll or stop decision:", roll_stop_decision)

                if roll_stop_decision == "roll":
                    dice_roll = roll_dice(player_strategy.rollable_dice_number)
                    print("dice roll:", dice_roll)
                    # check if it is possible for the player to pick any dice
                    dice_pick_check = check_if_player_can_pick_dice(dice_roll, player_strategy.dice_in_hand)
                    if dice_pick_check:
                        dice_pick_decision = player_strategy.decide_dice(dice_roll)
                        print("dice pick decision:", dice_pick_decision)

                        if dice_pick_decision not in dice_roll or dice_pick_decision in player_strategy.dice_in_hand:
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
                    player_turn_over = True

            # after the player's turn is over
            player_dice_sum = player_strategy.dice_sum()
            if "worm" in player_strategy.dice_in_hand:
                chosen_tile = get_closest_lower_tile(player_dice_sum, globals.active_tiles)
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

            # if there *is* a valid dice:
            # 1. remove it from active tiles
            # 2. add it to the player's tiles
            else:
                print("tile taken from active:", chosen_tile, "active tiles:", globals.active_tiles)
                globals.active_tiles.remove(chosen_tile)
                globals.player_tiles[player].append(chosen_tile)

            # stop the game if there are no active tiles left
            if len(globals.active_tiles) == 0:
                break

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

    sorted_ranked_list = sorted(ranked_list.items(), key=lambda x: x[1], reverse=True)

    for player in ranked_list:
        print(f"Player {player}: {ranked_list[player]} worms, tiles: {globals.player_tiles[player]}")


game()
