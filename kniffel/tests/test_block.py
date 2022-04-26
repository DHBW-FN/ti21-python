# pylint: disable=C
# pylint: disable=protected-access
import unittest
from unittest import mock
from unittest import TestCase
from unittest.mock import patch

import kniffel.game
from kniffel.game import Block, LowerBlock, UpperBlock, Kniffel, Dice


class TestBlock(TestCase):

    def setUp(self) -> None:
        self.block = Block()

    @patch.object(UpperBlock, 'evaluate', return_value=100)
    @patch.object(LowerBlock, 'evaluate', return_value=80)
    def test_evaluate2(self, mock_lower, mock_upper):
        self.block.kniffel_bonus = 0
        self.assertEqual(180, self.block.evaluate())

    @patch.object(UpperBlock, 'evaluate', return_value=100)
    @patch.object(LowerBlock, 'evaluate', return_value=80)
    def test_evaluate3(self, mock_lower, mock_upper):
        self.block.kniffel_bonus = 50
        self.assertEqual(230, self.block.evaluate())

    # @patch.object(Kniffel, 'evaluate', return_value=50)
    # @patch.object(Dice, 'count', return_value=5)
    # def test_submit(self, mock_dice_, mock_kniffel):
    #     mock_dice = mock.Mock()
    #     self.block.submit(mock_dice, 5)
    #     self.assertEqual(50, self.block.kniffel_bonus)


if __name__ == "__main__":
    unittest.main()
