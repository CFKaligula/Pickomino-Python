from random import choices, seed, sample
import player_strategies
import globals
from time import sleep
import os
import visualize
import sys

seed(71)


def roll_dice(num_dice):
    return choices(globals._DICE_OPTIONS, k=num_dice)


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
        # at the end of the loop, we have to check if the last active tile might be lower than num
        if last_tile < num:
            if globals.verbose:
                print(num, active_tiles)
            result = last_tile
    return result


def put_tile_back_in_active_tiles(tile, active_tiles):
    for i in range(len(active_tiles)):
        if active_tiles[i] > tile:
            # Move insertion into for-loop
            active_tiles.insert(i, tile)
            break
    return active_tiles


def let_player_roll(rollable_dice_number, player_strategy):
    player_turn_over = False
    # roll the dice
    dice_roll = roll_dice(rollable_dice_number)

    # visualize rolled dice
    if globals.verbose:
        print("dice roll:")
        visualize.visualize_dice(dice_roll)

    # check if it is possible for the player to pick any dice
    if not set(dice_roll).issubset(set(player_strategy.dice_in_hand)):
        dice_pick_decision = player_strategy.decide_dice(dice_roll)
        if globals.verbose:
            print("dice pick decision:", dice_pick_decision)

        # extra check if a valid die is chosen
        if dice_pick_decision not in dice_roll or dice_pick_decision in player_strategy.dice_in_hand:
            raise Exception("INVALID DICE PICK DECISION")
            input()

        # add chosen die from roll to player's hand and remove from rollabe dice
        chosen_dice_number = dice_roll.count(dice_pick_decision)
        player_strategy.dice_in_hand.extend([dice_pick_decision]*chosen_dice_number)
        rollable_dice_number -= chosen_dice_number

    else:
        if globals.verbose:
            print("Turn over, no dice to pick...",
                  "dice roll:", dice_roll,
                  "dice in hand:", player_strategy.dice_in_hand)
        player_turn_over = True

    return player_turn_over, rollable_dice_number


def player_loses_turn(player_name):
    # when there is no valid dice to pick:
    # 1. remove the top tile from the tiles of the player
    # 2. return it to active tiles
    # 3. remove highest active tile (unless the highest tile was returned)
    if len(globals.player_tiles[player_name]) > 0:
        returned_tile = globals.player_tiles[player_name][-1]
        globals.player_tiles[player_name].remove(returned_tile)
        globals.active_tiles = put_tile_back_in_active_tiles(returned_tile, globals.active_tiles)
        if returned_tile != globals.active_tiles[-1]:
            globals.active_tiles.pop(-1)
    else:
        # if there is no tile to take, just remove highest active tile
        globals.active_tiles.pop(-1)


def player_takes_tile(player_strategy, player_name):
    player_dice_sum = player_strategy.dice_sum()
    stealable_tiles_dict = globals.get_stealable_tiles_dict(player_name)
    # if there is a stealable tile
    if player_dice_sum in stealable_tiles_dict:
        if globals.verbose:
            print(f"tile {player_dice_sum} will be stolen", globals.player_tiles)
        player_name_to_be_stolen_from = stealable_tiles_dict[player_dice_sum]
        # remove it from player who currently owns it
        globals.player_tiles[player_name_to_be_stolen_from].remove(player_dice_sum)
        # add it to the player's tiles
        globals.player_tiles[player_name].append(player_dice_sum)
        if globals.verbose:
            print("tile is stolen", globals.player_tiles)
    # if the chosen tile is in the active tiles
    else:
        chosen_tile = get_closest_lower_tile(player_dice_sum, globals.active_tiles)
        if chosen_tile is None:
            # state that should be impossible to reach, just here for debug purpose
            input("how did we get here")
        if globals.verbose:
            print("tile to be taken from active:", chosen_tile, "active tiles:", globals.active_tiles)
        # remove it from active tiles
        globals.active_tiles.remove(chosen_tile)
        # add it to the player's tiles
        globals.player_tiles[player_name].append(chosen_tile)
        if globals.verbose:
            print("added tile", globals.player_tiles)


def decide_winner(round_num, shuffled_player_list):
    if globals.verbose:
        print(f"The game is over after {round_num} rounds!")
    ranked_list = {}
    for player_name in shuffled_player_list:
        total_worm_amount = 0
        for tile in globals.player_tiles[player_name]:
            # calculate number of worms on a tile
            worm_number = 1 + (tile - 21) // 4
            total_worm_amount += worm_number

        ranked_list[player_name] = total_worm_amount

    sorted_ranked_list = globals.sorted_dict(ranked_list)
    if globals.verbose:
        for player_name in sorted_ranked_list:
            print(f"Player {player_name}: {ranked_list[player_name]} worms, tiles: {globals.player_tiles[player_name]}")

    return list(sorted_ranked_list.keys())[0]


def game():
    # assign player strategies
    player_strategy_list = {globals.player_name_dict[i]: player_strategies.score_player(globals.player_name_dict[i])
                            for i in range(1, globals._NUMBER_OF_PLAYERS+1)}

    player_strategy_list[globals.player_name_dict[1]] = player_strategies.score_player(globals.player_name_dict[1])
    player_strategy_list[globals.player_name_dict[2]] = player_strategies.simple_player(globals.player_name_dict[2])
    '''
    player_strategy_list[globals.player_name_dict[3]] = player_strategies.simple_player(globals.player_name_dict[3])
    player_strategy_list[globals.player_name_dict[4]] = player_strategies.simple_thief(globals.player_name_dict[4])
    player_strategy_list[globals.player_name_dict[5]] = player_strategies.less_dumb_player(globals.player_name_dict[5])
    player_strategy_list[globals.player_name_dict[6]] = player_strategies.less_dumb_thief(globals.player_name_dict[6])

    '''
    # randomly shuffle players so there is no first player advantage consistenly
    shuffled_player_list = sample(globals._PLAYER_NAME_LIST, globals._NUMBER_OF_PLAYERS)
    if globals.verbose:
        print(shuffled_player_list)
    round_num = 1

    while len(globals.active_tiles) > 0:
        round_num += 1

        for player_name in shuffled_player_list:
            if globals.verbose:
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
                if globals.verbose:
                    print("dice in hand:")
                    visualize.visualize_dice(player_strategy.dice_in_hand)
                    print("total sum:", player_strategy.dice_sum())

                roll_stop_decision = player_strategy.decide_roll_or_stop()
                if globals.verbose:
                    print("roll or stop decision:", roll_stop_decision)

                # player decides to roll
                if roll_stop_decision == "roll":
                    player_turn_over, rollable_dice_number = let_player_roll(rollable_dice_number, player_strategy)

                # player has chosen to stop
                else:
                    player_stopped = True
                    player_turn_over = True

                ''' after the player's turn is over '''
            if ("worm" in player_strategy.dice_in_hand) and player_stopped:
                player_takes_tile(player_strategy, player_name)

            else:
                ''' player didn't stop in time or has no worm'''
                if globals.verbose:
                    print("Not allowed to pick tile, no worm or not stopped:",
                          "dice in hand:", player_strategy.dice_in_hand,
                          "stopped:", player_stopped)

                player_loses_turn(player_name)

            if globals.verbose:
                print(f"player {player_name} turn result:",
                      "dice in hand:",  player_strategy.dice_in_hand,
                      "dice sum:", player_strategy.dice_sum(),
                      "all player tiles:", globals.player_tiles)

            # stop the game if there are no active tiles left
            if len(globals.active_tiles) == 0:
                break

    return decide_winner(round_num, shuffled_player_list)


def analyze():
    winner_dict = {}
    for i in range(globals._NUMBER_OF_GAMES):

        if i % (globals._NUMBER_OF_GAMES/10) == 0:
            print("Game", i)
        breaker = False
        if breaker:
            if i == 220:
                globals.enablePrint()
            if i > 220:
                quit()

        winner = game()
        # reset active tiles and player tiles for new game
        globals.active_tiles = list(range(21, 37))
        globals.player_tiles = {globals._PLAYER_NAME_LIST[i]: [] for i in range(globals._NUMBER_OF_PLAYERS)}
        if winner in winner_dict:
            winner_dict[winner] += 1
        else:
            winner_dict[winner] = 1

    sorted_winner_dict = globals.sorted_dict(winner_dict)
    lines_to_write = []
    for player_name in sorted_winner_dict:
        lines_to_write.append(f"Player {player_name}: {sorted_winner_dict[player_name]} wins\n")
    wins = list(sorted_winner_dict.values())
    lines_to_write.append(str(sorted_winner_dict["een"] - sorted_winner_dict["twee"]))
    folder_path = os.path.dirname(__file__)
    analysis_file_path = os.path.join(folder_path, "analysis.txt")
    with open(analysis_file_path, "w") as analysis_file:
        analysis_file.writelines(lines_to_write)
    print(sorted_winner_dict)


if __name__ == '__main__':
    # game()
    analyze()
