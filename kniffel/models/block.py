"""
This file contains the Block class
"""
from kniffel.models.dice import Dice
from kniffel.models.lowerblock import LowerBlock
from kniffel.models.upperblock import UpperBlock


class Block:
    """
    Class for modelling a block
    """

    def __init__(self):
        self.upper = UpperBlock()
        self.lower = LowerBlock()
        self.kniffel_bonus = 0

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
