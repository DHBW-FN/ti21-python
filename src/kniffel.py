"""
Modelling and executing Kniffel
"""
from numpy import random


class Dice:
    """
    Class for modelling a dice
    """
    def __init__(self):
        self.dice = [Die(), Die(), Die(), Die(), Die()]

    def count(self, value: int):
        occurrences = 0
        for die in self.dice:
            if die.value == value:
                occurrences += 1
        return occurrences

    def roll(self):
        for die in self.dice:
            die.roll()

    def save(self, index: int):
        self.dice[index].save()

    def un_save(self, index: int):
        self.dice[index].un_save()


class Die:
    """
    Class for modelling a die
    """
    def __init__(self):
        self.value = 0
        self.saved = False

    def roll(self):
        if not self.saved:
            self.value = random.randint(1, 6)

    def save(self):
        self.saved = True

    def un_save(self):
        self.saved = False


class Kniffel:
    """
    Class for modelling a Kniffel game
    """
    def __init__(self, number_of_players: int):
        self.players = []
        for i in range(number_of_players):
            self.players.append(Player("Player " + str(i + 1)))
        self.active_player = self.players[0]

    def roll(self):
        self.active_player.roll()

    def save(self, die_index: int):
        self.active_player.save(die_index)


class Player:
    """
    Class for modelling a player
    """
    def __init__(self, username: str):
        self.username = username
        self.block = Block()
        self.dice = Dice()
        self.rolls = 0

    def roll(self):
        if self.rolls < 3:
            self.dice.roll()
            self.rolls += 1
            return
        else:
            raise Exception("You have already rolled 3 times")

    def save(self, die_index: int):
        self.dice.save(die_index)


class Block:
    """
    Class for modelling a block
    """
    def __init__(self):
        self.upper = UpperBlock()
        self.lower = LowerBlock()

    def evaluate(self):
        return self.upper.evaluate() + self.lower.evaluate()


class UpperBlock:
    """
    Class for modelling the upper block
    """
    def __init__(self):
        self.ones = UpperCategory("Ones", 1)
        self.twos = UpperCategory("Twos", 2)
        self.threes = UpperCategory("Threes", 3)
        self.fours = UpperCategory("Fours", 4)
        self.fives = UpperCategory("Fives", 5)
        self.sixes = UpperCategory("Sixes", 6)

    def evaluate(self):
        return 1


class LowerBlock:
    """
    Class for modelling the lower block
    """
    def __init__(self):
        self.three_of_a_kind = Dice()
        self.four_of_a_kind = Dice()
        self.full_house = Dice()
        self.small_straight = Dice()
        self.large_straight = Dice()
        self.kniffel = Dice()
        self.chance = Dice()

    def evaluate(self):
        return 1


class Category:
    """
    Class for modelling a category
    """
    def __init__(self, name: str):
        self.name = name
        self.dice = Dice()

    def submit(self, dice: Dice):
        self.dice = dice


class UpperCategory(Category):
    """
    Class for modelling an upper category
    """
    def __init__(self, name: str, category_value: int = 0):
        super().__init__(name)
        self.category_value = category_value

    def evaluate(self):
        return self.category_value * self.dice.count(self.category_value)


def main():
    kniffel = Kniffel(2)
    kniffel.roll()
    for die in kniffel.active_player.dice.dice:
        print(die.value)



if __name__ == "__main__":
    main()
