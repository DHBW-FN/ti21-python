# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase
from unittest.mock import patch

from kniffel.exceptions import InvalidCommandError
from kniffel.models.dice import Dice
from kniffel.models.player import Player


class TestPlayer(TestCase):

    def setUp(self) -> None:
        self.player = Player("test_player")

    def test_reset(self):
        block_old = self.player.block
        dice_old = self.player.dice
        self.player.reset()
        self.assertEqual(self.player.name, "test_player")
        self.assertEqual(self.player.rolls, 0)
        self.assertEqual(self.player.turns, 0)
        self.assertNotEqual(self.player.block, block_old)
        self.assertNotEqual(self.player.dice, dice_old)

    @patch.object(Dice, 'roll')
    def test_roll(self, _mock_dice):
        for i in range(3):
            self.player.roll()
            self.assertEqual(self.player.rolls, i+1)
        self.player.rolls = 3
        self.assertRaises(InvalidCommandError, self.player.roll)

    @patch.object(Dice, 'silent_roll')
    def test_silent_roll(self, _mock_dice):
        for i in range(3):
            self.player.silent_roll()
            self.assertEqual(self.player.rolls, i + 1)
        self.player.rolls = 3
        if not self.player.rolls < 3:
            self.assertRaises(InvalidCommandError, self.player.silent_roll)

    @patch("kniffel.models.dice.Dice.save")
    def test_save(self, _mock_save):
        self.player.save([1, 2, 3, 4, 5])
        _mock_save.assert_called()

    @patch("kniffel.models.dice.Dice.un_save")
    def test_un_save(self, _mock_un_save):
        self.player.un_save([1, 2, 3, 4, 5])
        _mock_un_save.assert_called()

    @patch("kniffel.models.block.Block.submit")
    def test_submit(self, _mock_submit):
        dice_old = self.player.dice
        self.player.submit(1)
        _mock_submit.assert_called()
        self.assertEqual(self.player.rolls, 0)
        self.assertNotEqual(self.player.dice, dice_old)

    @patch("kniffel.models.dice.Dice.print")
    def test_print_dice(self, _mock_print):
        self.player.print_dice()
        _mock_print.assert_called()

