from abc import ABC, abstractmethod
import globals


class abstract_player(ABC):

    def __init__(self):
        self.rollable_dice_number = 0
        self.dice_in_hand = []
        print("initalized ab player")
        pass

    @abstractmethod
    def decide_roll_or_stop(self):
        print("not implemented!")

    @abstractmethod
    def decide_dice(self, dice_roll):
        print("not implemented!")

    def dice_sum(self):
        sum = 0
        for die in self.dice_in_hand:
            if die == "worm":
                sum += 5
            else:
                sum += die
        return sum

    def check_valid_hand_to_pick_tile(self):
        return (self.dice_sum() >= globals.active_tiles[0]) and ("worm" in self.dice_in_hand)


class simple_player(abstract_player):
    def __init__(self):
        print("initlized simple player")
        super().__init__()

    def decide_roll_or_stop(self):
        result = "roll"
        if len(self.dice_in_hand) == 0:
            result = "roll"
        # if we have enough dice to pick the lowest tile and atleast one worm, stop
        elif self.check_valid_hand_to_pick_tile():
            result == "stop"

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
