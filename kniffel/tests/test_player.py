# pylint: disable=C
# pylint: disable=protected-access
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from kniffel.exceptions import InvalidCommandError
from kniffel.models.dice import Dice
from kniffel.models.player import Player, AIPlayer


class TestPlayer(TestCase):

    def setUp(self):
        self.player = Player("test_player")

    def test_reset(self):
        self.player = Player("test_player42")
        self.player.rolls = 42
        self.player.turns = 42

        old_block = self.player.block
        old_dice = self.player.dice
        self.player.reset()
        self.assertEqual(self.player.name, "test_player42")
        self.assertNotEqual(self.player.block, old_block)
        self.assertNotEqual(self.player.dice, old_dice)
        self.assertEqual(self.player.rolls, 0)
        self.assertEqual(self.player.turns, 0)

    @patch.object(Dice, 'roll')
    def test_roll(self, _mock_dice):
        for i in range(3):
            self.player.roll()
            self.assertEqual(self.player.rolls, i+1)
        self.assertRaises(InvalidCommandError, self.player.roll)

    @patch.object(Dice, 'silent_roll')
    def test_silent_roll(self, _mock_dice):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            for i in range(3):
                self.player.silent_roll()
                self.assertEqual(self.player.rolls, i + 1)
            self.assertRaises(InvalidCommandError, self.player.silent_roll)
            self.assertEqual(fake_out.getvalue(), "")

    @patch("kniffel.models.dice.Dice.save")
    def test_save(self, mock_save):
        self.player.save([1, 2, 3, 4, 5])
        mock_save.assert_called_with([1, 2, 3, 4, 5])

    @patch("kniffel.models.dice.Dice.un_save")
    def test_un_save(self, mock_un_save):
        self.player.un_save([1, 2, 3, 4, 5])
        mock_un_save.assert_called_with([1, 2, 3, 4, 5])

    @patch("kniffel.models.block.Block.submit")
    def test_submit(self, mock_submit):
        self.player.rolls = 3
        dice_old = self.player.dice

        self.player.submit(1)
        mock_submit.assert_called_with(dice_old, 1)
        self.assertNotEqual(self.player.dice, dice_old)
        self.assertEqual(self.player.rolls, 0)

    @patch("kniffel.models.dice.Dice.print")
    def test_print_dice(self, mock_print):
        self.player.print_dice()
        mock_print.assert_called()


class TestAIPlayer(TestCase):

    def setUp(self):
        self.player = AIPlayer("test_ai")

    @patch.object(Player, 'submit')
    def test_play(self, mock_submit):
        self.player.play()
        mock_submit.assert_called()

