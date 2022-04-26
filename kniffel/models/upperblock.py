"""
This file contains the UpperBlock class
"""
from kniffel.exceptions import InvalidIndexError
from kniffel.models.category import UpperCategory
from kniffel.models.dice import Dice


class UpperBlock:
    """
    Class for modelling the upper block
    """

    def __init__(self):
        self.ones = UpperCategory(1, "Ones", 1)
        self.twos = UpperCategory(2, "Twos", 2)
        self.threes = UpperCategory(3, "Threes", 3)
        self.fours = UpperCategory(4, "Fours", 4)
        self.fives = UpperCategory(5, "Fives", 5)
        self.sixes = UpperCategory(6, "Sixes", 6)

    def evaluate(self):
        """
        Evaluate the upper block return the total score
        :return:
        """
        total = 0
        for value in vars(self).items():
            if len(value) > 1:
                value = value[1]
            if isinstance(value, UpperCategory):
                total += value.evaluate()
        if total >= 63:
            return total + 35
        return total

    def submit(self, dice: Dice, category_index: int):
        """
        Submit a category
        :param dice:
        :param category_index:
        :return:
        """
        match category_index:
            case 1:
                self.ones.submit(dice)
            case 2:
                self.twos.submit(dice)
            case 3:
                self.threes.submit(dice)
            case 4:
                self.fours.submit(dice)
            case 5:
                self.fives.submit(dice)
            case 6:
                self.sixes.submit(dice)
            case _:
                raise InvalidIndexError()
