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

        with patch('sys.stdout', new=StringIO()) as fake_out:
            app.load_game(Path(os.path.join(curr_dir, "test.pkl")))
            mock_load.assert_called()
            self.assertIn("Loading game...", fake_out.getvalue())
            self.assertIn("Game loaded", fake_out.getvalue())

    def test_create_game(self):
        game = app.create_game()
        game.save_game()
        game_files = [file for file in os.listdir(Path(__file__).parent.parent.resolve()) if file.endswith(".pkl")]
        self.assertIn("game1.pkl", game_files)

    @patch('kniffel.app.create_game')
    def test_main_create_game1(self, _mock_create_game):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("1\n1\n1\n9")):
                app.main()
                self.assertIn("Welcome to Kniffel!", fake_out.getvalue())
                self.assertIn("Choose number of players:", fake_out.getvalue())
                self.assertIn("Choose number of AI players:", fake_out.getvalue())

    @patch('kniffel.app.create_game')
    def test_main_create_game2(self, _mock_create_game):
        # test value error for inputs
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("1\ns\nd\n9")):
                app.main()
                self.assertIn("Welcome to Kniffel!", fake_out.getvalue())
                self.assertIn("Invalid input!", fake_out.getvalue())

    @patch('kniffel.app.list_saved_games', return_value=["game1.pkl"])
    @patch('kniffel.app.load_game')
    def test_main_load_game1(self, mock_load_game, mock_list_saved_games):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("2\ngame1\n9")):
                app.main()
                self.assertIn("Welcome to Kniffel!", fake_out.getvalue())
                mock_list_saved_games.assert_called()
                mock_load_game.assert_called_with(Path("game1.pkl"))

    @patch('kniffel.app.list_saved_games', return_value=["game1.pkl"])
    def test_main_load_game2(self, _mock_list_saved_games):
        # test file not found error
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("2\nnew_game\n9")):
                app.main()
                self.assertIn("Welcome to Kniffel!", fake_out.getvalue())
                self.assertIn("Game not found!", fake_out.getvalue())

    @patch('kniffel.app.list_saved_games', return_value=[])
    def test_main_load_game3(self, _mock_list_saved_games):
        # test no save games available
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("2\n9")):
                app.main()
                self.assertIn("Welcome to Kniffel!", fake_out.getvalue())
                self.assertIn("No games available", fake_out.getvalue())

    @patch('kniffel.app.list_saved_games', return_value=["game1.pkl"])
    @patch('os.remove')
    def test_main_delete_game1(self, mock_remove, _mock_list_saved_games):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("3\ngame1\n9")):
                app.main()
                mock_remove.assert_called_with(Path("game1.pkl"))
                self.assertIn("Welcome to Kniffel!", fake_out.getvalue())
                self.assertIn("Game deleted", fake_out.getvalue())

    @patch('kniffel.app.list_saved_games', return_value=[])
    def test_main_delete_game2(self, _mock_list_saved_games):
        # test no save games available
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("3\n9")):
                app.main()
                self.assertIn("Welcome to Kniffel!", fake_out.getvalue())
                self.assertIn("No games available", fake_out.getvalue())

    @patch('kniffel.app.list_saved_games', return_value=["game1.pkl"])
    def test_main_delete_game3(self, _mock_list_saved_games):
        # test file not found error
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("3\ngame5\n9")):
                app.main()
                self.assertIn("Welcome to Kniffel!", fake_out.getvalue())
                self.assertIn("Game not found!", fake_out.getvalue())

    def test_main_invalid_command(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("42\n9")):
                app.main()
                self.assertIn("Welcome to Kniffel!", fake_out.getvalue())
                self.assertIn("Invalid command!", fake_out.getvalue())
