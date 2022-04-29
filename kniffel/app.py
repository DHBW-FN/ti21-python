"""
Modelling and executing Kniffel
"""
import os
import pickle
from pathlib import Path

from kniffel.models.game import Game


def list_save_games() -> list[bytes]:
    """
    List all saved games
    :return:
    """
    save_games = []
    curr_dir = Path(__file__).parent.resolve()
    for file in os.listdir(curr_dir):
        if file.endswith(".pkl"):
            save_games.append(file)
    return save_games


def print_save_games():
    """
    Print all saved games
    :return:
    """
    print("Available games:")
    for game in list_save_games():
        # print file name without extension
        print(f"\t{game.split('.')[0]}")


def load_game(path: Path) -> Game:
    """
    Load game from file
    :return:
    """
    print("Loading game...")
    with open(path, 'rb') as file:
        print("Game loaded!")
        return pickle.load(file)


def create_game(player_count: int = 1, ai_count: int = 1) -> Game:
    """
    Create game
    :return:
    """
    counter = 1

    curr_dir = Path(__file__).parent.resolve()
    game_path = os.path.join(curr_dir, f"game{counter}.pkl")
    while Path(game_path).exists():
        counter += 1
        game_path = os.path.join(curr_dir, f"game{counter}.pkl")

    game = Game(number_of_players=player_count, number_of_ai=ai_count, path=game_path)
    print(f"Game created at {game_path}")
    return game


def main():
    """
    Main function
    :return:
    """
    print("Welcome to Kniffel!")

    print("Available commands:"
          "\n\t[1] create - Create new game"
          "\n\t[2] load - Load game"
          "\n\t[3] delete - Delete game")
    match input("\nEnter command: "):
        case "create" | "1":
            print("Choose number of players:")
            number_of_players = input()
            print("Choose number of AI players:")
            number_of_ai = input()
            try:
                game = create_game(int(number_of_players), int(number_of_ai))
            except ValueError:
                print("Invalid input!")
                main()
        case "load" | "2":
            if len(list_save_games()) == 0:
                print("No games available")
                main()
            print_save_games()
            print("\nEnter game name:")
            game_name = input()
            game = load_game(Path(game_name + ".pkl"))
        case "delete" | "3":
            print_save_games()
            print("\nEnter game name:")
            game_name = input()
            Path(game_name + ".pkl").unlink()
            main()

    game.play()


if __name__ == "__main__":
    main()
