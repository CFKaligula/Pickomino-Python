from abc import ABC, abstractmethod
import globals


def get_counts_in_list(list):
    count_dict = {}
    for elem in list:
        if elem in count_dict:
            count_dict[elem] += elem
        else:
            count_dict[elem] = elem
    return count_dict


class abstract_player(ABC):

    def __init__(self, player_number):
        self.player_number = None
        self.dice_in_hand = []
        print("initalized ab player")
        pass

    @abstractmethod
    def decide_roll_or_stop(self):
        print("not implemented!")

    @abstractmethod
    def decide_dice(self, dice_roll):
        print("not implemented!")

    def duplicate_chance(self):
        unique_dice_in_hand = list(set(self.dice_in_hand))
        return len(unique_dice_in_hand)/6

    def dice_sum(self):
        sum = 0
        for die in self.dice_in_hand:
            if die == "worm":
                sum += 5
            else:
                sum += die
        return sum

    def check_valid_hand_to_pick_tile(self):
        stealable_stones = list(globals.get_stealable_stones_dict(self.player_number).keys())
        dice_sum = self.dice_sum()
        return ((dice_sum >= globals.active_tiles[0]) or dice_sum in stealable_stones) and ("worm" in self.dice_in_hand)


class simple_player(abstract_player):
    def __init__(self, *args):
        print("initlized simple player")
        super().__init__(args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        elif self.check_valid_hand_to_pick_tile():
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        result = 0
        # if we do not have a worm and a worm is in the dice roll, take it
        if "worm" in dice_roll and "worm" not in self.dice_in_hand:
            result = "worm"
        else:
            dice_roll_numbers = list(filter(lambda x: type(x) == int and x not in self.dice_in_hand, dice_roll))
            result = max(dice_roll_numbers)

        return result


class less_dumb_player(abstract_player):
    def __init__(self, *args):
        print("initlized smart player")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        elif self.check_valid_hand_to_pick_tile() and (self.duplicate_chance() >= 0.3 or self.dice_sum() > 30):
        #elif self.check_valid_hand_to_pick_tile():
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        dice_roll = list(filter(lambda x: x not in self.dice_in_hand, dice_roll))
        result = 0
        # if we do not have a worm and a worm is in the dice roll, take it
        worm_count = dice_roll.count("worm")
        # if there are only worms (wormcount == len dice roll), pick worm
        # otherwise pick worm for some other constraints
        if worm_count == len(dice_roll) or \
                ((worm_count > 2 or self.duplicate_chance() >= 0.3) and ("worm" not in self.dice_in_hand and "worm" in dice_roll)):
            result = "worm"
        else:
            dice_roll_numbers = list(filter(lambda x: type(x) == int and x not in self.dice_in_hand, dice_roll))
            count_dict = globals.sorted_dict(get_counts_in_list(dice_roll_numbers))
            print(count_dict)
            result = globals.key_with_max_val(count_dict)

        return result


class thief(abstract_player):
    def __init__(self, *args):
        print("initlized thief")
        super().__init__(*args)

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        # elif self.check_valid_hand_to_pick_tile() and (self.duplicate_chance() > 0.5 or self.dice_sum() > 30):
        elif self.check_valid_hand_to_pick_tile():
            result = "stop"

        return result

    def decide_dice(self, dice_roll):
        result = 0
        # if we do not have a worm and a worm is in the dice roll, take it
        if "worm" in dice_roll and "worm" not in self.dice_in_hand:
            result = "worm"
        else:
            dice_roll_numbers = list(filter(lambda x: type(x) == int and x not in self.dice_in_hand, dice_roll))
            stealable_stones = list(globals.get_stealable_stones_dict(self.player_number).keys())
            count_dict = globals.sorted_dict(get_counts_in_list(dice_roll_numbers))
            
            #check for every option whether taking it results in stealing
            for die_option in count_dict:
                if (self.dice_sum() + count_dict[die_option]) in stealable_stones:
                    result = die_option
                    print("STEAL TIME",count_dict, stealable_stones)
                    break

            else:
                # if we found no chance to steal, just take largest sum
                result = globals.key_with_max_val(count_dict)

        return result
