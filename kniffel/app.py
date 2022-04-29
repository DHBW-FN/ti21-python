"""
Modelling and executing Kniffel
"""
import pickle
from pathlib import Path

from kniffel.models.game import Game


def main():
    """
    Main function
    :return:
    """
    file_name = "\\game.pkl"

    curr_dir = Path(__file__).parent.resolve()
    game_file = str(curr_dir)+file_name

    path = Path(game_file)
    if path.exists():
        print("Loading game...")
        with open(path, "rb") as file:
            game = pickle.load(file)
        print("Game loaded!")
    else:
        print("Creating new game...")
        game = Game(1, 1)
        print("Game created!")

    game.play()


if __name__ == "__main__":
    main()
