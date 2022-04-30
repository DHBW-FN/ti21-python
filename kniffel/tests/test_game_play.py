# pylint: disable=C
# pylint: disable=protected-access
from io import StringIO
from unittest.mock import patch

from parameterized import parameterized

from kniffel.tests.test_game import TestGame


class TestGamePlay(TestGame):

    def test_play(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO("9")):
                self.game.play()
                self.assertIn("Enter command:", fake_out.getvalue())
                self.assertFalse(self.game.is_running)

    @parameterized.expand([
        ("value_error", "submit niklas", "invalid literal for int() with base 10: 'niklas'"),
        ("empty_command", "", "Invalid input."),
        ("invalid_argument", "save -1", "Invalid argument"),
        ("invalid_index", "submit -1", "Invalid index"),
        ("invalid_command_error", "0\n0\n0", "You have already rolled 3 times"),
    ])
    def test_play_error(self, _name, command, expected_string):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO(command + "\n9")):
                self.game.play()
                self.assertIn(expected_string, fake_out.getvalue())