# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase
from io import StringIO
from unittest.mock import patch

from parameterized import parameterized

from kniffel.models.game import Game
from kniffel.exceptions import InvalidInputError

# Missing methods: (display_message), (show_help), play (just a part is already tested), save_game, roll, save, un_save, print_dice, show_score,


class TestGame(TestCase):
    def setUp(self):
        self.game = Game(1, 1)

    @patch("kniffel.models.player.Player.roll")
    def test_init(self, mock_roll):
        self.game.__init__(1, 1)
        mock_roll.assert_called()

    @patch("kniffel.models.player.Player.end_turn")
    def test_play(self, mock_end_turn):
        self.game.play()
        mock_end_turn.assert_called()

    @patch("kniffel.models.player.Player.roll")
    def test_reset(self, mock_roll):
        self.game.reset()
        mock_roll.assert_called()

    @patch("kniffel.models.game.Game.end_turn")
    def test_submit(self, mock_roll):
        self.game.submit(1)
        mock_roll.assert_called()

    @patch("kniffel.models.game.Game.roll")
    def test_end_turn(self, mock_roll):
        self.game.end_turn()
        mock_roll.assert_called()

    @patch("kniffel.models.game.sys.exit")
    def test_end_game(self, mock_save):
        self.game.end_game()
        mock_save.assert_called()

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

    @patch("kniffel.models.game.Game.roll")
    def test_process_command_roll(self, mock_roll):
        self.game.process_command("0")
        mock_roll.assert_called()

    @patch("kniffel.models.game.Game.save")
    def test_process_command_save(self, mock_save):
        self.game.process_command("1 1")
        mock_save.assert_called()

    @patch("kniffel.models.game.Game.un_save")
    def test_process_command_unsave(self, mock_unsave):
        self.game.process_command("2 1")
        mock_unsave.assert_called()

    @patch("kniffel.models.game.Game.submit")
    def test_process_command_submit(self, mock_save):
        self.game.process_command("3 1")
        mock_save.assert_called()

    @patch("kniffel.models.game.show_help")
    def test_process_command_help(self, mock_save):
        self.game.process_command("4")
        mock_save.assert_called()

    @patch("kniffel.models.game.Game.show_score")
    def test_process_command_score(self, mock_save):
        self.game.process_command("5")
        mock_save.assert_called()

    @patch("kniffel.models.game.Game.print_dice")
    def test_process_command_printdice(self, mock_save):
        self.game.process_command("6")
        mock_save.assert_called()

    @patch("kniffel.models.game.Game.reset")
    def test_process_command_reset(self, mock_save):
        self.game.process_command("7")
        mock_save.assert_called()

    @patch("kniffel.models.game.sys.exit")
    def test_process_command_exit(self, mock_save):
        self.game.process_command("9")
        mock_save.assert_called()

    def test_process_command_wrong_command(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game.process_command("fake input")
            self.assertEqual(fake_out.getvalue(), "Unknown command: fake\n")
