# pylint: disable=C
# pylint: disable=protected-access
import os
from io import StringIO
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from kniffel import app


class TestApp(TestCase):

    def tearDown(self) -> None:
        curr_dir = Path(__file__).parent.parent.resolve()
        for file in os.listdir(curr_dir):
            if file.endswith(".pkl"):
                print(f"Deleting {file}")
                os.remove(os.path.join(curr_dir, file))

    def test_list_saved_games(self):
        # create 2 .pkl files in the current directory
        curr_dir = Path(__file__).parent.parent.resolve()
        for i in range(2):
            with open(os.path.join(curr_dir, f"test_{i}.pkl"), "w", encoding="UTF-8") as file:
                file.write("")
        self.assertEqual(2, len(app.list_saved_games()))
        self.assertEqual("['test_0.pkl', 'test_1.pkl']", str(app.list_saved_games()))

    def test_print_save_games(self):
        # create 2 .pkl files in the current directory
        curr_dir = Path(__file__).parent.parent.resolve()
        for i in range(2):
            with open(os.path.join(curr_dir, f"test_{i}.pkl"), "w", encoding="UTF-8") as file:
                file.write("")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            app.print_save_games()
            self.assertIn("Available games:", fake_out.getvalue())
            self.assertIn("test_0", fake_out.getvalue())
            self.assertIn("test_1", fake_out.getvalue())

    @patch('pickle.load')
    def test_load_game(self, mock_load):
        # create 1 .pkl files in the current directory
        curr_dir = Path(__file__).parent.parent.resolve()
        with open(os.path.join(curr_dir, "test.pkl"), "w", encoding="UTF-8") as file:
            file.write("")

        app.load_game(Path(os.path.join(curr_dir, "test.pkl")))
        mock_load.assert_called()

    def test_create_game(self):
        game = app.create_game()
        game.save_game()
        game_files = [file for file in os.listdir(Path(__file__).parent.parent.resolve()) if file.endswith(".pkl")]
        self.assertIn("game1.pkl", game_files)
