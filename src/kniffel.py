"""
Modelling and executing Kniffel
"""
import random


class Dice:
    def __init__(self):
        self.dice = [Die()] * 5

    def count(self, value: int):
        for die in self.dice:
            if die.value == value:
                return 1

    def roll(self):
        for die in self.dice:
            if not die.save:
                die.roll()


class Die:
    def __init__(self):
        self.value = 0
        self.save = False

    def roll(self):
        self.value = random.randint(1, 6)


class Kniffel:
    def __init__(self, number_of_players: int):
        self.players = []
        for i in range(number_of_players):
            self.players.append(Player("Player " + str(i + 1)))
        self.active_player = self.players[0]


class Player:
    def __init__(self, username: str):
        self.username = username
        self.block = Block()
        self.dice = Dice()
        self.rolls = 0

    def roll(self):
        self.dice.roll()
        self.rolls += 1


class Block:
    def __init__(self):
        self.upper = UpperBlock()
        self.lower = LowerBlock()

    def evaluate(self):
        return self.upper.evaluate() + self.lower.evaluate()


class UpperBlock:
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
    def __init__(self, name: str):
        self.name = name
        self.dice = Dice()

    def submit(self, dice: Dice):
        self.dice = dice


class UpperCategory(Category):
    def __init__(self, name: str, category_value: int = 0):
        super().__init__(name)
        self.category_value = category_value

    def evaluate(self):
        return self.category_value * self.dice.count(self.category_value)


def main():
    dice = Dice()
    print(dice.dice[0].value)


if __name__ == "__main__":
    main()
