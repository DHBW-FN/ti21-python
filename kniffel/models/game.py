"""
This file contains the Game class and some helping functions
"""
import pickle
import sys

from prettytable import PrettyTable

from kniffel.exceptions import InvalidInputError, InvalidArgumentError, CategoryAlreadyFilledError, \
    InvalidCommandError, InvalidIndexError
from kniffel.models.player import Player, AIPlayer


def display_message(message):
    """
    Display an error message to the user
    :param message:
    :return:
    """

    print("\033[93m" + str(message) + "\033[0m")
    # input("Press enter to continue...")


def show_help():
    """
    Show help for the game
    :return:
    """
    print(
        "Commands:\n"
        "[0] roll: Roll the dice\n"
        "[1] save <die_index>: Save the die with the given index[1-5]\n"
        "[2] un_save <die_index>: Unsave the die with the given index[1-5]\n"
        "[3] submit <category_index>: Submit the score for the given category\n"
        "[4] help: Show this help message\n"
        "[5] score: Show the current game state\n"
        "[6] dice: Show the current dice state\n"
        "[7] reset: Reset the game\n"
        "[9] exit: Exit the game\n"
    )


class Game:
    """
    Class for modelling a Kniffel game
    """

    def __init__(self, number_of_players: int, number_of_ai: int, path: str = "game.pkl"):
        self.is_running = True
        self.path = path
        self.players = []
        for i in range(number_of_players):
            self.players.append(Player("Player " + str(i + 1)))
        for i in range(number_of_ai):
            self.players.append(AIPlayer("AI " + str(i + 1)))
        self.active_player = self.players[0]
        self.active_player.turns += 1
        self.active_player.roll()

    def play(self):
        """
        Play the game
        :return:
        """
        while self.is_running:
            self.save_game()

            if isinstance(self.active_player, AIPlayer):
                self.active_player.play()
                self.end_turn()
                continue

            try:
                self.process_command(input(f"[{self.active_player.name}] Enter command: "))
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
            except CategoryAlreadyFilledError:
                display_message("Category already filled.")

    def save_game(self):
        """
        Save the game
        :return:
        """
        with open(self.path, "wb") as file:
            pickle.dump(self, file)

    def reset(self):
        """
        Reset the game
        :return:
        """
        for player in self.players:
            player.reset()
        self.active_player = self.players[0]
        self.active_player.turns += 1
        self.active_player.roll()
        print("Game reset")

    def roll(self):
        """
        Roll the dice
        :return:
        """
        return self.active_player.roll()

    def save(self, die_indices: list[int]):
        """
        Save the die with the given index
        :param die_indices:
        :return:
        """
        self.active_player.save(die_indices)

    def un_save(self, die_indices: list[int]):
        """
        Unsave the die with the given index
        :param die_indices:
        :return:
        """
        self.active_player.un_save(die_indices)

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

        if self.active_player.turns > 13:
            self.end_game()
        self.show_score()
        print("*" * 20)
        print(self.active_player.name + " is now playing")
        self.roll()

    def print_dice(self):
        """
        Print the dice
        """
        self.active_player.print_dice()

    def show_score(self):
        """
        Show the current scoreboard
        :return:
        """
        my_table = PrettyTable(["Id", "Categories"] + [player.name for player in self.players])
        my_table.add_row([self.active_player.block.upper.ones.index, self.active_player.block.upper.ones.name] +
                         [str(player.block.upper.ones.evaluate())
                          if player.block.upper.ones.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.twos.index, self.active_player.block.upper.twos.name] +
                         [str(player.block.upper.twos.evaluate())
                          if player.block.upper.twos.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.threes.index, self.active_player.block.upper.threes.name] +
                         [str(player.block.upper.threes.evaluate())
                          if player.block.upper.threes.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.fours.index, self.active_player.block.upper.fours.name] +
                         [str(player.block.upper.fours.evaluate())
                          if player.block.upper.fours.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.fives.index, self.active_player.block.upper.fives.name] +
                         [str(player.block.upper.fives.evaluate())
                          if player.block.upper.fives.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.upper.sixes.index, self.active_player.block.upper.sixes.name] +
                         [str(player.block.upper.sixes.evaluate())
                          if player.block.upper.sixes.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row(["==", "Total Upper"] + [str(player.block.upper.evaluate()) for player in self.players])
        my_table.add_row([self.active_player.block.lower.three_of_a_kind.index, self.active_player.block.lower.three_of_a_kind.name] +
                         [str(player.block.lower.three_of_a_kind.evaluate())
                          if player.block.lower.three_of_a_kind.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.four_of_a_kind.index, self.active_player.block.lower.four_of_a_kind.name] +
                         [str(player.block.lower.four_of_a_kind.evaluate())
                          if player.block.lower.four_of_a_kind.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.full_house.index, self.active_player.block.lower.full_house.name] +
                         [str(player.block.lower.full_house.evaluate())
                          if player.block.lower.full_house.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.small_straight.index, self.active_player.block.lower.small_straight.name] +
                         [str(player.block.lower.small_straight.evaluate())
                          if player.block.lower.small_straight.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.large_straight.index, self.active_player.block.lower.large_straight.name] +
                         [str(player.block.lower.large_straight.evaluate())
                          if player.block.lower.large_straight.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.kniffel.index, self.active_player.block.lower.kniffel.name] +
                         [str(player.block.lower.kniffel.evaluate())
                          if player.block.lower.kniffel.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row([self.active_player.block.lower.chance.index, self.active_player.block.lower.chance.name] +
                         [str(player.block.lower.chance.evaluate())
                          if player.block.lower.chance.dice.count(0) == 0
                          else "-" for player in self.players])
        my_table.add_row(["==", "Total Lower"] +
                         [str(player.block.lower.evaluate()) for player in self.players])
        my_table.add_row(["==", "Kniffel-Bonus"] +
                         [str(player.block.kniffel_bonus) for player in self.players])
        my_table.add_row(["==", "Total"] +
                         [str(player.block.evaluate()) for player in self.players])
        print(my_table)

    def end_game(self):
        """
        End the game.
        """
        print("*" * 20)
        print("\nGame over!\n")
        print("*" * 20)
        self.show_score()
        print("\nThanks for playing!")
        sys.exit(0)

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
            case "roll" | "0":
                self.roll()
            case "save" | "1":
                if not arguments:
                    raise InvalidInputError()
                self.save(list(map(int, arguments)))
            case "un-save" | "2":
                if not arguments:
                    raise InvalidInputError()
                self.un_save(list(map(int, arguments)))
            case "submit" | "3":
                if not arguments:
                    raise InvalidInputError()
                self.submit(int(arguments[0]))
            case "help" | "4":
                show_help()
            case "score" | "5":
                self.show_score()
            case "dice" | "6":
                self.print_dice()
            case "reset" | "7":
                self.reset()
            case "exit" | "9":
                sys.exit(0)
            case _:
                print("Unknown command: " + command)
