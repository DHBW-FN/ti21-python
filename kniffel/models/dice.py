"""
This  file contains the Dice class
"""
from prettytable import PrettyTable

from kniffel.exceptions import InvalidArgumentError
from kniffel.models.die import Die


class Dice:
    """
    Class for modelling a dice
    """

    def __init__(self, amount: int = 5):
        self.dice = [Die() for _ in range(amount)]

    def __str__(self):
        return str([die.value for die in self.dice])

    def count(self, value: int):
        """
        Count the number of dice with the given value
        :param value:
        :return:
        """
        occurrences = 0
        for die in self.dice:
            if die.value == value:
                occurrences += 1
        return occurrences

    def includes(self, value: int):
        """
        Check if the dice contains a die with the given value
        :param value:
        :return:
        """
        for die in self.dice:
            if die.value == value:
                return True
        return False

    def roll(self):
        """
        Roll all dice
        :return:
        """
        self.silent_roll()
        print("Rolled the dice!")
        self.print()
        return list(die.value for die in self.dice)

    def silent_roll(self):
        """
        Roll all dice without displaying the result
        :return:
        """
        for die in self.dice:
            die.roll()
        return list(die.value for die in self.dice)

    def save(self, indices: list[int]):
        """
        Save the die at the given index 1-5
        :param indices:
        :return:
        """
        for index in indices:
            if index > len(self.dice) or index < 1:
                raise InvalidArgumentError()
            self.dice[index - 1].save()
        self.print()

    def un_save(self, indices: list[int]):
        """
        Un-save the die at the given index 1-5
        :param indices:
        :return:
        """
        for index in indices:
            if index > len(self.dice) or index < 1:
                raise InvalidArgumentError()
            self.dice[index - 1].un_save()
        self.print()

    def is_rolled(self) -> bool:
        """
        Check if the category is filled
        :return:
        """
        return self.dice[0].value != 0

    def print(self):
        """
        Print the dice and show the saved status
        """
        my_table = PrettyTable(["Dice Number"] + [str(i + 1) for i in range(len(self.dice))])
        my_table.add_row(["Dice Value"] + [str(die.value) for die in self.dice])
        my_table.add_row(["Saved"] + [str(die.saved) for die in self.dice])

        print(my_table)
