# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase
from io import StringIO
from unittest.mock import patch

from parameterized import parameterized

from kniffel.models.game import Game
from kniffel.exceptions import InvalidInputError


class TestGame(TestCase):
    def setUp(self):
        self.game = Game(1, 1)

    @parameterized.expand([
        ("save_no_argument", "save", InvalidInputError),
        ("un-save_no_argument", "un-save", InvalidInputError),
        ("submit_no_argument", "submit", InvalidInputError)
    ])
    def test_process_command_no_argument(self, _name, command, expected_error):
        self.assertRaises(expected_error, lambda: self.game.process_command(command))

    def test_process_command_empty(self):
        with self.assertRaises(InvalidInputError):
            self.game.process_command("")

    def test_process_command_wrong_command(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game.process_command("fake input")
            self.assertEqual(fake_out.getvalue(), "Unknown command: fake\n")

    @patch("kniffel.models.game.Game.roll")
    def test_process_command_roll(self, mock_roll):
        self.game.process_command("roll")
        mock_roll.assert_called()

    @patch("kniffel.models.game.Game.save")
    def test_process_command_save(self, mock_save):
        self.game.process_command("save 1")
        mock_save.assert_called()

