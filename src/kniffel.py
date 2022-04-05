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

    def includes(self, value: int):
        for die in self.dice:
            if die.value == value:
                return True
        return False

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

    def submit(self, category_index: int):
        self.active_player.submit(category_index)
        self.active_player = self.players[(self.players.index(self.active_player) + 1) % len(self.players)]


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

    def submit(self, category_index: int):
        self.block.submit(self.dice, category_index)


class Block:
    """
    Class for modelling a block
    """

    def __init__(self):
        self.upper = UpperBlock()
        self.lower = LowerBlock()

    def evaluate(self):
        return self.upper.evaluate() + self.lower.evaluate()

    def submit(self, dice: Dice, category_index: int):
        if category_index <= 6:
            self.upper.submit(dice, category_index)
        else:
            self.lower.submit(dice, category_index)


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
        total = 0
        for value in vars(self).items():
            if isinstance(value, UpperCategory):
                total += value.evaluate()
        if total >= 63:
            return total + 35
        return total

    def submit(self, dice: Dice, category_index: int):
        if category_index == 1:
            self.ones.submit(dice)
        elif category_index == 2:
            self.twos.submit(dice)
        elif category_index == 3:
            self.threes.submit(dice)
        elif category_index == 4:
            self.fours.submit(dice)
        elif category_index == 5:
            self.fives.submit(dice)
        elif category_index == 6:
            self.sixes.submit(dice)
        else:
            raise Exception("Invalid category index")


class LowerBlock:
    """
    Class for modelling the lower block
    """

    def __init__(self):
        self.three_of_a_kind = Category("Three of a kind")
        self.four_of_a_kind = Category("Four of a kind")
        self.full_house = Category("Full house")
        self.small_straight = Category("Small straight")
        self.large_straight = Category("Large straight")
        self.kniffel = Category("Kniffel")
        self.chance = Category("Chance")

    def evaluate(self):
        total = 0
        for value in vars(self).items():
            if isinstance(value, UpperCategory):
                total += value.evaluate()
        return total

    def submit(self, dice: Dice, category_index: int):
        if category_index == 7:
            self.three_of_a_kind.submit(dice)
        elif category_index == 8:
            self.four_of_a_kind.submit(dice)
        elif category_index == 9:
            self.full_house.submit(dice)
        elif category_index == 10:
            self.small_straight.submit(dice)
        elif category_index == 11:
            self.large_straight.submit(dice)
        elif category_index == 12:
            self.kniffel.submit(dice)
        elif category_index == 13:
            self.chance.submit(dice)
        else:
            raise Exception("Invalid category index")


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


class LowerCategory(Category):
    """
    Class for modelling a lower category
    """
    def __init__(self, name: str):
        super().__init__(name)


class ThreeOfAKind(LowerCategory):

    def __init__(self, name: str):
        super().__init__(name)

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) >= 3:
                return i * 3


class FourOfAKind(LowerCategory):

    def __init__(self, name: str):
        super().__init__(name)

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) >= 4:
                return i * 4


def main():
    kniffel = Kniffel(2)
    print(kniffel.active_player.block.upper.evaluate())
    for die in kniffel.active_player.dice.dice:
        print(die.value)


if __name__ == "__main__":
    main()
