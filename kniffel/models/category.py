"""
This file contains the Category classes
"""
from abc import abstractmethod, ABCMeta

from kniffel.exceptions import CategoryAlreadyFilledError
from kniffel.models.dice import Dice


class Category:
    """
    Class for modelling a category
    """

    def __init__(self, index: int, name: str):
        self.name = name
        self.dice = Dice()
        self.index = index

    def submit(self, dice: Dice):
        """
        Submit a category
        :param dice:
        :return:
        """
        if self.dice.is_rolled():
            raise CategoryAlreadyFilledError()
        self.dice = dice
        print("Submitted " + str(dice) + " to " + self.name + " for a score of " + str(self.evaluate()))

    @abstractmethod
    def evaluate(self):
        """
        Evaluate the category return the score
        :return:
        """

    def test_evaluate(self, dice: Dice):
        """
        Evaluate the category return the score
        :return:
        """
        if self.dice.is_rolled():
            return -1
        self.dice = dice
        value = self.evaluate()
        self.dice = Dice()
        return value


class UpperCategory(Category):
    """
    Class for modelling an upper category
    """

    def __init__(self, index: int, name: str, category_value: int = 0):
        super().__init__(index, name)
        self.category_value = category_value

    def evaluate(self):
        return self.category_value * self.dice.count(self.category_value)


class LowerCategory(Category, metaclass=ABCMeta):
    """
    Class for modelling a lower category
    """


class ThreeOfAKind(LowerCategory):
    """
    Class for modelling a three of a kind category
    """

    def evaluate(self):
        for i in range(1, 7):
            if self.dice.count(i) >= 3:
                total = 0
                for j in range(5):
                    total += self.dice.dice[j].value
                return total
        return 0


class FourOfAKind(LowerCategory):
    """
    Class for modelling a four of a kind category
    """

    def evaluate(self):
        for i in range(1, 7):
            if self.dice.count(i) >= 4:
                total = 0
                for j in range(5):
                    total += self.dice.dice[j].value
                return total
        return 0


class FullHouse(LowerCategory):
    """
    Class for modelling a full house category
    """

    def evaluate(self):
        for i in range(1, 7):
            if self.dice.count(i) == 3:
                for j in range(1, 7):
                    if (self.dice.count(j)) == 2 and (i != j):
                        return 25
        return 0


class SmallStraight(LowerCategory):
    """
    Class for modelling a small straight category
    """

    def evaluate(self):
        for i in range(1, 4):
            if self.dice.count(i) >= 1:
                for j in range(i + 1, i + 4):
                    if self.dice.count(j) == 0:
                        break
                else:
                    return 30
        return 0


class LargeStraight(LowerCategory):
    """
    Class for modelling a large straight category
    """

    def evaluate(self):
        for i in range(1, 3):
            if self.dice.count(i) >= 1:
                for j in range(i + 1, i + 5):
                    if self.dice.count(j) == 0:
                        return 0
                return 40
        return 0


class Kniffel(LowerCategory):
    """
    Class for modelling a kniffel category
    """

    def evaluate(self):
        for i in range(1, 7):
            if self.dice.count(i) == 5:
                return 50
        return 0


class Chance(LowerCategory):
    """
    Class for modelling a chance category
    """

    def evaluate(self):
        total = 0
        for i in range(5):
            total += self.dice.dice[i].value
        return total
