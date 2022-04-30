"""
This file contains the Block class
"""
from kniffel.exceptions import InvalidIndexError
from kniffel.models.category import ThreeOfAKind, FourOfAKind, FullHouse, SmallStraight, LargeStraight, Kniffel, \
    Chance, UpperCategory, LowerCategory
from kniffel.models.dice import Dice


class Block:
    """
    Class for modelling a block
    """

    def __init__(self):
        self.upper: UpperBlock = UpperBlock()
        self.lower: LowerBlock = LowerBlock()
        self.kniffel_bonus: int = 0

    def evaluate(self):
        """
        Evaluate the block return the total score
        :return:
        """
        return self.upper.evaluate() + self.lower.evaluate() + self.kniffel_bonus

    def submit(self, dice: Dice, category_index: int):
        """
        Submit a category
        :param dice:
        :param category_index:
        :return:
        """
        if category_index <= 6:
            self.upper.submit(dice, category_index)
            if self.lower.kniffel.evaluate() > 0:
                if dice.count(category_index) == 5:
                    print("You just earned a Kniffel-Bonus! +50 points")
                    self.kniffel_bonus += 50
        else:
            self.lower.submit(dice, category_index)


class UpperBlock:
    """
    Class for modelling the upper block
    """

    def __init__(self):
        self.ones: UpperCategory = UpperCategory(1, "Ones", 1)
        self.twos: UpperCategory = UpperCategory(2, "Twos", 2)
        self.threes: UpperCategory = UpperCategory(3, "Threes", 3)
        self.fours: UpperCategory = UpperCategory(4, "Fours", 4)
        self.fives: UpperCategory = UpperCategory(5, "Fives", 5)
        self.sixes: UpperCategory = UpperCategory(6, "Sixes", 6)

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


class LowerBlock:
    """
    Class for modelling the lower block
    """

    def __init__(self):
        self.three_of_a_kind: ThreeOfAKind = ThreeOfAKind(7, "Three of a kind")
        self.four_of_a_kind: FourOfAKind = FourOfAKind(8, "Four of a kind")
        self.full_house: FullHouse = FullHouse(9, "Full house")
        self.small_straight: SmallStraight = SmallStraight(10, "Small straight")
        self.large_straight: LargeStraight = LargeStraight(11, "Large straight")
        self.kniffel: Kniffel = Kniffel(12, "Kniffel")
        self.chance: Chance = Chance(13, "Chance")

    def evaluate(self):
        """
        Evaluate the lower block return the total score
        :return:
        """
        total = 0
        for value in vars(self).items():
            if len(value) > 1:
                value = value[1]
            if isinstance(value, LowerCategory):
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
