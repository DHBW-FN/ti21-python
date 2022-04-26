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

    path = Path("game.pkl")
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
