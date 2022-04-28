# pylint: disable=C
# pylint: disable=protected-access
import unittest
from unittest import mock
from unittest import TestCase
from unittest.mock import patch

from kniffel.models.block import Block, LowerBlock, UpperBlock
from kniffel.models.dice import Dice
from kniffel.models.category import Kniffel


class TestBlock(TestCase):

    def setUp(self) -> None:
        self.block = Block()

    @patch.object(UpperBlock, 'evaluate', return_value=100)
    @patch.object(LowerBlock, 'evaluate', return_value=80)
    def test_evaluate1(self, mock_lower, mock_upper):
        self.block.kniffel_bonus = 0
        self.assertEqual(180, self.block.evaluate())

    @patch.object(UpperBlock, 'evaluate', return_value=100)
    @patch.object(LowerBlock, 'evaluate', return_value=80)
    def test_evaluate2(self, mock_lower, mock_upper):
        self.block.kniffel_bonus = 50
        self.assertEqual(230, self.block.evaluate())

    @patch.object(Kniffel, 'evaluate', return_value=50)
    @patch.object(Dice, 'count', return_value=5)
    def test_submit(self, mock_dice_, mock_kniffel):
        self.Dice = mock.Mock()
        self.Dice.count.return_value = 5
        self.block.submit(self.Dice, 5)
        self.assertEqual(50, self.block.kniffel_bonus)

    @patch('kniffel.models.block.UpperBlock.submit')
    def test_upper_submit(self, mock_upper_submit):
        self.Dice = mock.Mock()
        self.block.submit(self.Dice, 4)
        mock_upper_submit.assert_called()

    @patch('kniffel.models.block.LowerBlock.submit')
    def test_lower_submit(self, mock_lower_submit):
        self.Dice = mock.Mock()
        self.block.submit(self.Dice, 7)
        mock_lower_submit.assert_called()


if __name__ == "__main__":
    unittest.main()
