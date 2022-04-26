"""
This file contains the Player and AIPlayer class
"""
from kniffel.exceptions import InvalidCommandError
from kniffel.models.category import Category
from kniffel.models.dice import Dice
from kniffel.models.block import Block, UpperBlock, LowerBlock


class Player:
    """
    Class for modelling a player
    """

    def __init__(self, name: str):
        self.name = name
        self.block = Block()
        self.dice = Dice()
        self.rolls = 0
        self.turns = 0

    def reset(self):
        """
        Reset the player
        """
        self.__init__(self.name)

    def roll(self):
        """
        Roll the dice
        :return:
        """
        if self.rolls < 3:
            self.rolls += 1
            return self.dice.roll()
        raise InvalidCommandError("You have already rolled 3 times")

    def silent_roll(self):
        """
        Roll the dice without showing the dice
        :return:
        """
        if self.rolls < 3:
            self.rolls += 1
            return self.dice.silent_roll()
        raise InvalidCommandError("You have already rolled 3 times")

    def save(self, die_indices: list[int]):
        """
        Save a die
        :param die_indices:
        :return:
        """
        self.dice.save(die_indices)

    def un_save(self, die_indices: list[int]):
        """
        Un-save a die
        :param die_indices:
        :return:
        """
        self.dice.un_save(die_indices)

    def submit(self, category_index: int):
        """
        Submit a category
        :param category_index:
        :return:
        """
        self.block.submit(self.dice, category_index)
        self.dice = Dice()
        self.rolls = 0

    def print_dice(self):
        """
        Print the dice
        """
        self.dice.print()


class AIPlayer(Player):
    """
    Class for modelling an AI player
    """

    def play(self):
        """
        Play a turn
        :return:
        """
        best_index = -1
        best_score = -1
        for value in vars(self.block).items():
            if isinstance(value[1], (UpperBlock, LowerBlock)):
                for category in vars(value[1]).items():
                    if isinstance(category[1], Category):
                        if category[1].test_evaluate(self.dice) >= best_score:
                            best_score = category[1].test_evaluate(self.dice)
                            best_index = category[1].index

        # if best_score < 10 and self.rolls < 3:
        #     self.silent_roll()
        #     self.play()

        self.submit(best_index)
