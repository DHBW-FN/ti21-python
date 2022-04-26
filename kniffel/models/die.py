"""
This file contains the Die class
"""
from numpy import random


class Die:
    """
    Class for modelling a die
    """

    def __init__(self, value=0, saved=False):
        self.value = value
        self.saved = saved

    def __eq__(self, other):
        if not isinstance(other, Die):
            return False
        return self.value == other.value and self.saved == other.saved

    def roll(self):
        """
        Roll the die
        :return:
        """
        if not self.saved:
            self.value = random.randint(1, 7)
        return self.value

    def save(self):
        """
        Save the die
        :return:
        """
        self.saved = True

    def un_save(self):
        """
        Un-save the die
        :return:
        """
        self.saved = False
