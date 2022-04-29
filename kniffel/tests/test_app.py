# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase
from unittest.mock import patch
from io import StringIO

from kniffel.app import main


class TestApp(TestCase):

    @patch('kniffel.models.game.Game.play')
    @patch('pickle.load')
    @patch('pathlib.Path.exists', return_value=True)
    def test_path_exists(self, _mock_exists, mock_load, _mock_play):
        # check if prints are being executed if path exists
        # check if game.play is called if path exists

        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            expected_text = "Loading game...\nGame loaded!\n"
            self.assertEqual(fake_out.getvalue(), expected_text)
        mock_load.assert_called()

    @patch('kniffel.models.game.Game.play')
    @patch('kniffel.models.dice.Dice.roll')
    @patch('pathlib.Path.exists')
    def test_path_not_exists(self, mock_exists, mock_dice, mock_play):
        # check if prints are being executed if path doesn't exist
        # check if game.play is called if path doesn't exist
        mock_dice.return_value = ""
        mock_exists.return_value = False
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            expected_text = "Creating new game...\nGame created!\n"
            self.assertEqual(fake_out.getvalue(), expected_text)
        mock_play.assert_called()
