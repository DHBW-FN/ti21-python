"""
Modelling and executing Kniffel
"""
import sys

from numpy import random

from kniffel.exceptions import InvalidInputError, InvalidArgumentError, InvalidIndexError, InvalidCommandError


def display_message(message):
    print("\033[93m" + str(message) + "\033[0m")
    # input("Press enter to continue...")


class Dice:
    """
    Class for modelling a dice
    """

    def __init__(self):
        self.dice = [Die(), Die(), Die(), Die(), Die()]

    def __str__(self):
        return str([die.value for die in self.dice])

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
        print("Rolled: " + str([die.value for die in self.dice]))

    def save(self, index: int):
        if index > len(self.dice) or index < 1:
            raise InvalidArgumentError()
        self.dice[index - 1].save()

    def un_save(self, index: int):
        if index > len(self.dice):
            raise InvalidArgumentError()
        self.dice[index].un_save()


class Die:
    """
    Class for modelling a die
    """

    def __init__(self):
        self.value = random.randint(1, 6)
        self.saved = False

    def roll(self):
        if not self.saved:
            self.value = random.randint(1, 6)

    def save(self):
        print("Saved: " + str(self.value))
        self.saved = True

    def un_save(self):
        self.saved = False


def show_help():
    print(
        "Commands:\n"
        "[0] roll: Roll the dice\n"
        "[1] save <die_index>: Save the die with the given index[1-6]\n"
        "[2] submit <category_index>: Submit the score for the given category\n"
        "[3] help: Show this help message\n"
        "[4] score: Show the current game state\n"
        "[5] dice: Show the current dice state\n"
        "[9] exit: Exit the game\n"
    )


class Game:
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
        self.end_turn()

    def end_turn(self):
        self.active_player = self.players[(self.players.index(self.active_player) + 1) % len(self.players)]
        self.active_player.turns += 1
        self.roll()

    def show_dice(self):
        print("Dice: " + str([die.value for die in self.active_player.dice.dice]))
        print("Saved: " + str([die.saved for die in self.active_player.dice.dice]))

    def show_score(self):
        print("Score:")
        for player in self.players:
            print(player.username + ": " + str(player.block.evaluate()))

    def process_command(self, command_str: str):
        if command_str == "":
            raise InvalidInputError()
        command = command_str.split()[0]
        arguments = command_str.split()[1:]

        match command:
            case "roll":
                self.roll()
            case "save":
                if not arguments:
                    raise InvalidInputError()
                self.save(int(arguments[0]))
            case "submit":
                if not arguments:
                    raise InvalidInputError()
                self.submit(int(arguments[0]))
            case "help":
                show_help()
            case "score":
                self.show_score()
            case "dice":
                self.show_dice()
            case "exit":
                sys.exit(0)
            case _:
                print("Unknown command: " + command)


class Player:
    """
    Class for modelling a player
    """

    def __init__(self, username: str):
        self.username = username
        self.block = Block()
        self.dice = Dice()
        self.turns = 0
        self.rolls = 1

    def roll(self):
        if self.rolls < 3:
            self.dice.roll()
            self.rolls += 1
            return
        raise InvalidCommandError("You have already rolled 3 times")

    def save(self, die_index: int):
        self.dice.save(die_index)

    def submit(self, category_index: int):
        self.block.submit(self.dice, category_index)
        self.rolls = 1


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
        self.three_of_a_kind = ThreeOfAKind("Three of a kind")
        self.four_of_a_kind = FourOfAKind("Four of a kind")
        self.full_house = FullHouse("Full house")
        self.small_straight = SmallStraight("Small straight")
        self.large_straight = LargeStraight("Large straight")
        self.kniffel = Kniffel("Kniffel")
        self.chance = Chance("Chance")

    def evaluate(self):
        total = 0
        for value in vars(self).items():
            if isinstance(value, UpperCategory):
                total += value.evaluate()
        return total

    def submit(self, dice: Dice, category_index: int):
        match category_index:
            case 1:
                self.three_of_a_kind.submit(dice)
            case 2:
                self.four_of_a_kind.submit(dice)
            case 3:
                self.full_house.submit(dice)
            case 4:
                self.small_straight.submit(dice)
            case 5:
                self.large_straight.submit(dice)
            case 6:
                self.kniffel.submit(dice)
            case 7:
                self.chance.submit(dice)
            case _:
                raise InvalidIndexError()


class Category:
    """
    Class for modelling a category
    """

    def __init__(self, name: str):
        self.name = name
        self.dice = Dice()

    def submit(self, dice: Dice):
        self.dice = dice
        print("Submitted " + str(dice) + " to " + self.name + " for a score of " + str(self.evaluate()))

    def evaluate(self):
        pass


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


class ThreeOfAKind(LowerCategory):

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) >= 3:
                total = 0
                for j in range(5):
                    total += self.dice.dice[j].value
                return total
        return 0


class FourOfAKind(LowerCategory):

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) >= 4:
                total = 0
                for j in range(5):
                    total += self.dice.dice[j].value
                return total
        return 0


class FullHouse(LowerCategory):

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) == 3:
                for j in range(1, 6):
                    if self.dice.count(j) == 2 & i != j:
                        return 25
        return 0


class SmallStraight(LowerCategory):

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) == 1:
                for j in range(i + 1, i + 4):
                    if self.dice.count(j) == 1:
                        return 30
        return 0


class LargeStraight(LowerCategory):

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) == 1:
                for j in range(i + 1, i + 5):
                    if self.dice.count(j) == 1:
                        return 40
        return 0


class Kniffel(LowerCategory):

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) == 5:
                return 50
        return 0


class Chance(LowerCategory):

    def evaluate(self):
        total = 0
        for i in range(5):
            total += self.dice.dice[i].value
        return total


def main():
    game = Game(2)
    while True:
        try:
            game.process_command(input("Enter command: "))
        except ValueError as error:
            display_message(error)
        except InvalidInputError:
            display_message("Invalid input.")
        except InvalidArgumentError:
            display_message("Invalid argument.")
        except InvalidIndexError:
            display_message("Invalid index.")
        except InvalidCommandError as error:
            display_message(error)


if __name__ == "__main__":
    main()
