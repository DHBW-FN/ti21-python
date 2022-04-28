# pylint: disable=C
# pylint: disable=protected-access
import os.path
from unittest import TestCase
from io import StringIO
from unittest.mock import patch

from parameterized import parameterized

from kniffel.models.game import Game
from kniffel.exceptions import InvalidInputError


class TestGame(TestCase):
    def setUp(self):
        self.game = Game(1, 1)

    def tearDown(self):
        if os.path.exists("game.pkl"):
            os.remove("game.pkl")

    @patch("kniffel.models.game.pickle.dump")
    def test_save_game(self, mock_dump):
        self.game.save_game()
        mock_dump.assert_called()

    @patch("kniffel.models.player.Player.reset")
    def test_reset(self, mock_reset):
        old_turns = self.game.active_player.turns
        self.game.reset()
        mock_reset.assert_called()
        self.assertEqual(self.game.players[0], self.game.active_player)
        self.assertEqual(old_turns + 1, self.game.active_player.turns)
        self.assertTrue(self.game.active_player.dice.dice[0].value != 0)

    @patch("kniffel.models.player.Player.roll")
    def test_roll(self, mock_roll):
        self.game.roll()
        mock_roll.assert_called()

    @patch("kniffel.models.player.Player.save")
    def test_save(self, mock_save):
        self.game.save([1, 3])
        mock_save.assert_called_with([1, 3])

    @patch("kniffel.models.player.Player.un_save")
    def test_un_save(self, mock_un_save):
        self.game.un_save([1, 3])
        mock_un_save.assert_called_with([1, 3])

    @patch("kniffel.models.player.Player.submit")
    @patch("kniffel.models.game.Game.end_turn")
    def test_submit(self, mock_roll, mock_submit):
        self.game.submit(1)
        mock_submit.assert_called_with(1)
        mock_roll.assert_called()

    @patch("kniffel.models.game.Game.show_score")
    @patch("kniffel.models.game.Game.roll")
    def test_end_turn(self, mock_roll, mock_show_score):
        old_active_player = self.game.active_player
        self.game.end_turn()
        self.assertEqual(self.game.players[
                             (self.game.players.index(old_active_player) + 1) % len(self.game.players)],
                         self.game.active_player, "Next player should be the next in the list")
        self.assertTrue(self.game.active_player.turns == 1, "Turns should be increased")
        mock_show_score.assert_called()
        mock_roll.assert_called()

    @patch("kniffel.models.game.Game.show_score")
    @patch("kniffel.models.game.sys.exit")
    def test_end_game(self, mock_save, mock_show_score):
        self.game.end_game()
        mock_save.assert_called_with(0)
        mock_show_score.assert_called()

    @parameterized.expand([
        ("save_no_argument", "save", InvalidInputError),
        ("save_no_argument", "1", InvalidInputError),
        ("un-save_no_argument", "un-save", InvalidInputError),
        ("un-save_no_argument", "2", InvalidInputError),
        ("submit_no_argument", "submit", InvalidInputError),
        ("submit_no_argument", "3", InvalidInputError),
        ("nothing", "", InvalidInputError)
    ])
    def test_process_command_no_argument(self, _name, command, expected_error):
        self.assertRaises(expected_error, self.game.process_command, command)

    @patch("kniffel.models.game.Game.roll")
    def test_process_command_roll(self, mock_roll):
        self.game.process_command("0")
        mock_roll.assert_called()

    @patch("kniffel.models.game.Game.save")
    def test_process_command_save(self, mock_save):
        self.game.process_command("save 1 2 3")
        mock_save.assert_called_with([1, 2, 3])

    @patch("kniffel.models.game.Game.un_save")
    def test_process_command_un_save(self, mock_un_save):
        self.game.process_command("un-save 1 2 3")
        mock_un_save.assert_called_with([1, 2, 3])

    @patch("kniffel.models.game.Game.submit")
    def test_process_command_submit(self, mock_submit):
        self.game.process_command("3 1")
        mock_submit.assert_called_with(1)

    @patch("kniffel.models.game.show_help")
    def test_process_command_help(self, mock_help):
        self.game.process_command("4")
        mock_help.assert_called()

    @patch("kniffel.models.game.Game.show_score")
    def test_process_command_score(self, mock_show_score):
        self.game.process_command("5")
        mock_show_score.assert_called()

    @patch("kniffel.models.game.Game.print_dice")
    def test_process_command_print_dice(self, mock_print_dice):
        self.game.process_command("6")
        mock_print_dice.assert_called()

    @patch("kniffel.models.game.Game.reset")
    def test_process_command_reset(self, mock_reset):
        self.game.process_command("7")
        mock_reset.assert_called()

    def test_process_command_wrong_command(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game.process_command("fake input")
            self.assertEqual(fake_out.getvalue(), "Unknown command: fake\n")
