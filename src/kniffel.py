"""
Modelling and executing Kniffel
"""
import random


class Kniffel:
    def __init__(self, number_of_players: int):
        self.players = []
        for i in range(number_of_players):
            self.players.append(Player("Player " + str(i + 1)))
        self.active_player = self.players[0]


class Player:
    def __init__(self, username: str):
        self.username = username


class Block:
    def __init__(self):
        self.upper = UpperBlock()
        self.lower = LowerBlock()

    def evaluate(self):
        return self.upper.evaluate() + self.lower.evaluate()


class UpperBlock:
    def __init__(self):
        self.ones = 0
        self.twos = 0
        self.threes = 0
        self.fours = 0
        self.fives = 0
        self.sixes = 0

    def evaluate(self):
        return 1


class LowerBlock:
    def __init__(self):
        self.three_of_a_kind = 0
        self.four_of_a_kind = 0
        self.full_house = 0
        self.small_straight = 0
        self.large_straight = 0
        self.yahtzee = 0
        self.chance = 0

    def evaluate(self):
        return 1


class Dice:
    def __init__(self):
        self.dice = [Die()] * 5

    def count(self, value: int):
        for die in self.dice:
            if die.value == value:
                return 1


class Die:
    def __init__(self):
        self.value = 0
        self.save = False

    def roll(self):
        self.value = random.randint(1, 6)


def main():
    dice = Dice()
    print(dice.dice[0].value)


if __name__ == "__main__":
    main()
