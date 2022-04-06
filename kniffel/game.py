"""
Modelling and executing Kniffel
"""
import pickle
import sys
from pathlib import Path

from numpy import random
from prettytable import PrettyTable

from kniffel.exceptions import InvalidInputError, InvalidArgumentError, InvalidIndexError, InvalidCommandError


def display_message(message):
    """
    Display an error message to the user
    :param message:
    :return:
    """

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
        print("Rolled: " + str([die.value for die in self.dice]))

    def silent_roll(self):
        """
        Roll all dice without displaying the result
        :return:
        """
        for die in self.dice:
            die.roll()

    def save(self, index: int):
        """
        Save the die at the given index 1-5
        :param index:
        :return:
        """
        if index > len(self.dice) or index < 1:
            raise InvalidArgumentError()
        self.dice[index - 1].save()

    def un_save(self, index: int):
        """
        Un-save the die at the given index 1-5
        :param index:
        :return:
        """
        if index > len(self.dice) or index < 1:
            raise InvalidArgumentError()
        self.dice[index - 1].un_save()


class Die:
    """
    Class for modelling a die
    """

    def __init__(self):
        self.value = 0
        self.saved = False

    def roll(self):
        """
        Roll the die
        :return:
        """
        if not self.saved:
            self.value = random.randint(1, 6)

    def save(self):
        """
        Save the die
        :return:
        """
        print("Saved: " + str(self.value))
        self.saved = True

    def un_save(self):
        """
        Unsave the die
        :return:
        """
        print("Unsaved: " + str(self.value))
        self.saved = False


def show_help():
    """
    Show help for the game
    :return:
    """
    print(
        "Commands:\n"
        "[0] roll: Roll the dice\n"
        "[1] save <die_index>: Save the die with the given index[1-5]\n"
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
        self.active_player.roll()

    def roll(self):
        """
        Roll the dice
        :return:
        """
        self.active_player.roll()

    def save(self, die_index: int):
        """
        Save the die with the given index
        :param die_index:
        :return:
        """
        self.active_player.save(die_index)

    def un_save(self, die_index: int):
        """
        Unsave the die with the given index
        :param die_index:
        :return:
        """
        self.active_player.un_save(die_index)

    def submit(self, category_index: int):
        """
        Submit the score for the given category
        :param category_index:
        :return:
        """
        self.active_player.submit(category_index)
        self.end_turn()

    def end_turn(self):
        """
        End the current turn
        :return:
        """
        self.active_player = self.players[(self.players.index(self.active_player) + 1) % len(self.players)]
        self.active_player.turns += 1
        print("The new score is:")
        self.show_score()
        print("*" * 20)
        print(self.active_player.username + " is now playing")
        self.roll()

    def show_dice(self):
        """
        Show the dice values and if they are saved
        :return:
        """
        print("Dice: " + str([die.value for die in self.active_player.dice.dice]) + " Rolls: " + str(self.active_player.rolls))
        print("Saved: " + str([die.saved for die in self.active_player.dice.dice]))

    def show_score(self):
        """
        Show the current scoreboard
        :return:
        """
        print("Score:")
        for player in self.players:
            print(player.username + ": " + str(player.block.evaluate()))

        my_table = PrettyTable(["Id", "Categories"] + [player.username for player in self.players])
        my_table.add_row([self.active_player.block.upper.ones.index, "Ones"] +
                         [str(player.block.upper.ones.evaluate())
                          if player.block.upper.ones.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.twos.index, "Twos"] +
                         [str(player.block.upper.twos.evaluate())
                          if player.block.upper.twos.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.threes.index, "Threes"] +
                         [str(player.block.upper.threes.evaluate())
                          if player.block.upper.threes.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.fours.index, "Fours"] +
                         [str(player.block.upper.fours.evaluate())
                          if player.block.upper.fours.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.fives.index, "Fives"] +
                         [str(player.block.upper.fives.evaluate())
                          if player.block.upper.fives.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.sixes.index, "Sixes"] +
                         [str(player.block.upper.sixes.evaluate())
                          if player.block.upper.sixes.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row(["==", "Total Upper"] + [str(player.block.upper.evaluate()) for player in self.players])
        my_table.add_row([self.active_player.block.lower.three_of_a_kind.index, "Three of a kind"] +
                         [str(player.block.lower.three_of_a_kind.evaluate())
                          if player.block.lower.three_of_a_kind.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.four_of_a_kind.index, "Four of a kind"] +
                         [str(player.block.lower.four_of_a_kind.evaluate())
                          if player.block.lower.four_of_a_kind.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.full_house.index, "Full House"] +
                         [str(player.block.lower.full_house.evaluate())
                          if player.block.lower.full_house.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.small_straight.index, "Small Straight"] +
                         [str(player.block.lower.small_straight.evaluate())
                          if player.block.lower.small_straight.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.large_straight.index, "Large Straight"] +
                         [str(player.block.lower.large_straight.evaluate())
                          if player.block.lower.large_straight.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.kniffel.index, "Kniffel"] +
                         [str(player.block.lower.kniffel.evaluate())
                          if player.block.lower.kniffel.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.chance.index, "Chance"] +
                         [str(player.block.lower.chance.evaluate())
                          if player.block.lower.chance.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row(["==", "Total Lower"] +
                         [str(player.block.lower.evaluate()) for player in self.players])
        my_table.add_row(["==", "Total"] +
                         [str(player.block.evaluate()) for player in self.players])
        print(my_table)

    def process_command(self, command_str: str):
        """
        Process a command string
        :param command_str:
        :return:
        """
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
            case "un-save":
                if not arguments:
                    raise InvalidInputError()
                self.un_save(int(arguments[0]))
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
        self.rolls = 0
        self.turns = 0

    def roll(self):
        """
        Roll the dice
        :return:
        """
        if self.rolls < 3:
            self.dice.roll()
            self.rolls += 1
            return
        raise InvalidCommandError("You have already rolled 3 times")

    def silent_roll(self):
        """
        Roll the dice without showing the dice
        :return:
        """
        if self.rolls < 3:
            self.dice.silent_roll()
            self.rolls += 1
            return
        raise InvalidCommandError("You have already rolled 3 times")

    def save(self, die_index: int):
        """
        Save a die
        :param die_index:
        :return:
        """
        self.dice.save(die_index)

    def un_save(self, die_index: int):
        """
        Un-save a die
        :param die_index:
        :return:
        """
        self.dice.un_save(die_index)

    def submit(self, category_index: int):
        """
        Submit a category
        :param category_index:
        :return:
        """
        self.block.submit(self.dice, category_index)
        self.dice = Dice()
        self.rolls = 0


class Block:
    """
    Class for modelling a block
    """

    def __init__(self):
        self.upper = UpperBlock()
        self.lower = LowerBlock()

    def evaluate(self):
        """
        Evaluate the block return the total score
        :return:
        """
        return self.upper.evaluate() + self.lower.evaluate()

    def submit(self, dice: Dice, category_index: int):
        """
        Submit a category
        :param dice:
        :param category_index:
        :return:
        """
        if category_index <= 6:
            self.upper.submit(dice, category_index)
        else:
            self.lower.submit(dice, category_index)


class UpperBlock:
    """
    Class for modelling the upper block
    """

    def __init__(self):
        self.ones = UpperCategory(1, "Ones", 1)
        self.twos = UpperCategory(2, "Twos", 2)
        self.threes = UpperCategory(3, "Threes", 3)
        self.fours = UpperCategory(4, "Fours", 4)
        self.fives = UpperCategory(5, "Fives", 5)
        self.sixes = UpperCategory(6, "Sixes", 6)

    def evaluate(self):
        """
        Evaluate the upper block return the total score
        :return:
        """
        total = 0
        for value in vars(self).items():
            if isinstance(value, UpperCategory):
                total += value.evaluate()
        if total >= 63:
            return total + 35
        return total

    def submit(self, dice: Dice, category_index: int):
        """
        Submit a category
        :param dice:
        :param category_index:
        :return:
        """
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
        self.three_of_a_kind = ThreeOfAKind(7, "Three of a kind")
        self.four_of_a_kind = FourOfAKind(8, "Four of a kind")
        self.full_house = FullHouse(9, "Full house")
        self.small_straight = SmallStraight(10, "Small straight")
        self.large_straight = LargeStraight(11, "Large straight")
        self.kniffel = Kniffel(12, "Kniffel")
        self.chance = Chance(13, "Chance")

    def evaluate(self):
        """
        Evaluate the lower block return the total score
        :return:
        """
        total = 0
        for value in vars(self).items():
            if isinstance(value, UpperCategory):
                total += value.evaluate()
        return total

    def submit(self, dice: Dice, category_index: int):
        """
        Submit a category
        :param dice:
        :param category_index:
        :return:
        """
        match category_index:
            case 7:
                self.three_of_a_kind.submit(dice)
            case 8:
                self.four_of_a_kind.submit(dice)
            case 9:
                self.full_house.submit(dice)
            case 10:
                self.small_straight.submit(dice)
            case 11:
                self.large_straight.submit(dice)
            case 12:
                self.kniffel.submit(dice)
            case 13:
                self.chance.submit(dice)
            case _:
                raise InvalidIndexError()


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
        self.dice = dice
        print("Submitted " + str(dice) + " to " + self.name + " for a score of " + str(self.evaluate()))

    def evaluate(self):
        """
        Evaluate the category return the score
        :return:
        """
        raise NotImplementedError()


class UpperCategory(Category):
    """
    Class for modelling an upper category
    """

    def __init__(self, index: int, name: str, category_value: int = 0):
        super().__init__(index, name)
        self.category_value = category_value

    def evaluate(self):
        return self.category_value * self.dice.count(self.category_value)


class LowerCategory(Category):
    """
    Class for modelling a lower category
    """

    def evaluate(self):
        pass


class ThreeOfAKind(LowerCategory):
    """
    Class for modelling a three of a kind category
    """

    def evaluate(self):
        for i in range(1, 6):
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
        for i in range(1, 6):
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
        for i in range(1, 6):
            if self.dice.count(i) == 3:
                for j in range(1, 6):
                    if self.dice.count(j) == 2 & i != j:
                        return 25
        return 0


class SmallStraight(LowerCategory):
    """
    Class for modelling a small straight category
    """

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) == 1:
                for j in range(i + 1, i + 4):
                    if self.dice.count(j) == 1:
                        return 30
        return 0


class LargeStraight(LowerCategory):
    """
    Class for modelling a large straight category
    """

    def evaluate(self):
        for i in range(1, 6):
            if self.dice.count(i) == 1:
                for j in range(i + 1, i + 5):
                    if self.dice.count(j) == 1:
                        return 40
        return 0


class Kniffel(LowerCategory):
    """
    Class for modelling a kniffel category
    """

    def evaluate(self):
        for i in range(1, 6):
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


def main():
    """
    Main function
    :return:
    """
    game = Game(2)

    path = Path("game.pkl")
    if path.exists():
        with open(path, "rb") as file:
            game = pickle.load(file)

    while True:
        with open(path, "wb") as file:
            pickle.dump(game, file)

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
