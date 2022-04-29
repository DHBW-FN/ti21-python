from unittest import TestCase
from unittest.mock import patch
from io import StringIO

from kniffel.app import main


class TestApp(TestCase):

    @patch('pathlib.Path.exists')
    def test_path_exists(self, mock_exists):
        mock_exists.return_value = True
        with patch('kniffel.models.game.Game.play'):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                expected_text = "Loading game...\nGame loaded!\n"
                self.assertEqual(fake_out.getvalue(), expected_text)

    @patch('kniffel.models.dice.Dice.roll')
    @patch('pathlib.Path.exists')
    def test_path_not_exists(self, mock_exists, mock_dice):
        mock_dice.return_value = ""
        mock_exists.return_value = False
        with patch('kniffel.models.game.Game.play'):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                expected_text = "Creating new game...\nGame created!\n"
                self.assertEqual(fake_out.getvalue(), expected_text)

    @patch('kniffel.models.game.Game.play')
    @patch('pathlib.Path.exists')
    def test_play_called1(self, mock_exists, mock_play):
        mock_exists.return_value = True
        main()
        mock_play.assert_called()

    @patch('kniffel.models.game.Game.play')
    @patch('pathlib.Path.exists')
    def test_play_called2(self, mock_exists, mock_play):
        mock_exists.return_value = False
        main()
        mock_play.assert_called()
