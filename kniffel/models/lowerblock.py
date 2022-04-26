"""
This file contains the LowerBlock class
"""
from kniffel.exceptions import InvalidIndexError
from kniffel.models.category import Category, ThreeOfAKind, FourOfAKind, FullHouse, SmallStraight, LargeStraight, \
    Kniffel, Chance
from kniffel.models.dice import Dice


class LowerBlock:
    """
    Class for modelling the lower block
    """

    def __init__(self):
        self.three_of_a_kind = ThreeOfAKind(7, "Three of a kind")
        self.four_of_a_kind = FourOfAKind(8, "Four of a kind")
        self.full_house = FullHouse(9, "Full house")
        self.small_straight = SmallStraight(10, "Small straight")
        self.large_straight = LargeStraight(11, "Large straight")
        self.kniffel = Kniffel(12, "Kniffel")
        self.chance = Chance(13, "Chance")

    def evaluate(self):
        """
        Evaluate the lower block return the total score
        :return:
        """
        total = 0
        for value in vars(self).items():
            if len(value) > 1:
                value = value[1]
            if isinstance(value, Category):
                total += value.evaluate()
        return total

    def submit(self, dice: Dice, category_index: int):
        """
        Submit a category
        :param dice:
        :param category_index:
        :return:
        """
        match category_index:
            case 7:
                self.three_of_a_kind.submit(dice)
            case 8:
                self.four_of_a_kind.submit(dice)
            case 9:
                self.full_house.submit(dice)
            case 10:
                self.small_straight.submit(dice)
            case 11:
                self.large_straight.submit(dice)
            case 12:
                self.kniffel.submit(dice)
            case 13:
                self.chance.submit(dice)
            case _:
                raise InvalidIndexError()
