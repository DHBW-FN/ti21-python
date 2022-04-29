# pylint: disable=C
# pylint: disable=protected-access
from unittest import mock
from unittest import TestCase
from unittest.mock import patch, call

from kniffel.models.block import Block, LowerBlock, UpperBlock
from kniffel.models.dice import Dice
from kniffel.models.category import Kniffel
import kniffel.exceptions


class TestBlock(TestCase):

    def setUp(self):
        self.block = Block()

    @patch.object(UpperBlock, 'evaluate', return_value=100)
    @patch.object(LowerBlock, 'evaluate', return_value=80)
    def test_evaluate1(self, _mock_lower, _mock_upper):
        self.block.kniffel_bonus = 0
        self.assertEqual(180, self.block.evaluate())

    @patch.object(UpperBlock, 'evaluate', return_value=100)
    @patch.object(LowerBlock, 'evaluate', return_value=80)
    def test_evaluate2(self, _mock_lower, _mock_upper):
        self.block.kniffel_bonus = 50
        self.assertEqual(230, self.block.evaluate())

    @patch.object(Kniffel, 'evaluate', return_value=50)
    def test_submit(self, _mock_kniffel):
        self.block.submit(Dice(values=[1, 1, 1, 1, 1]), 1)
        self.assertEqual(50, self.block.kniffel_bonus)

    @patch('kniffel.models.block.UpperBlock.submit')
    def test_upper_submit(self, mock_upper_submit):
        mock_dice = mock.Mock()
        self.block.submit(mock_dice, 4)
        mock_upper_submit.assert_called_with(mock_dice, 4)

    @patch('kniffel.models.block.LowerBlock.submit')
    def test_lower_submit(self, mock_lower_submit):
        mock_dice = mock.Mock()
        self.block.submit(mock_dice, 7)
        mock_lower_submit.assert_called_with(mock_dice, 7)


class TestUpperBlock(TestCase):

    def setUp(self):
        self.upper_block = UpperBlock()

    @patch('kniffel.models.category.UpperCategory.evaluate', return_value=12)
    def test_evaluate(self, mock_evaluate):
        # check if upper bonus is added
        # return_value is evaluated value of each dice
        # so return_value * 6 + 35
        self.assertEqual(107, self.upper_block.evaluate())
        mock_evaluate.assert_called()

    @patch('kniffel.models.category.UpperCategory.evaluate', return_value=6)
    def test_evaluate2(self, mock_evaluate):
        # check if dice values are added without bonus
        # return_value is evaluated value of each dice
        # so return_value * 6
        self.assertEqual(36, self.upper_block.evaluate())
        mock_evaluate.assert_called()

    @patch('kniffel.models.category.UpperCategory.submit')
    def test_submit(self, mock_submit):
        # check if the submit method is called for every dice
        # with a dice object
        mock_dice = mock.Mock()
        for i in range(1, 7):
            self.upper_block.submit(mock_dice, i)
        calls = [
            call(mock_dice),
        ]
        mock_submit.assert_has_calls(calls=calls)

    @patch('kniffel.models.category.UpperCategory.submit')
    def test_submit_2(self, _mock_submit):
        # check if the submit method is called n times
        # once for each die
        mock_dice = mock.Mock()
        call_count = 0
        for i in range(1, 7):
            self.upper_block.submit(mock_dice, i)
            call_count += 1
        self.assertEqual(6, call_count)

    def test_submit_3(self):
        # check if the exception is raised if index out of range
        mock_dice = mock.Mock()
        self.assertRaises(kniffel.exceptions.InvalidIndexError, self.upper_block.submit, mock_dice, 7)


class TestLowerBlock(TestCase):

    def setUp(self):
        self.lower_block = LowerBlock()

    @patch('kniffel.models.category.ThreeOfAKind.evaluate', return_value=1)
    @patch('kniffel.models.category.FourOfAKind.evaluate', return_value=2)
    @patch('kniffel.models.category.FullHouse.evaluate', return_value=3)
    @patch('kniffel.models.category.SmallStraight.evaluate', return_value=4)
    @patch('kniffel.models.category.LargeStraight.evaluate', return_value=5)
    @patch('kniffel.models.category.Kniffel.evaluate', return_value=6)
    @patch('kniffel.models.category.Chance.evaluate', return_value=7)
    def test_evaluate(
                        self,
                        *args
                      ):
        # check if dice values are added together
        # and if each method is called
        self.assertEqual(28, self.lower_block.evaluate())
        for arg in args:
            arg.assert_called()

    @patch('kniffel.models.category.LowerCategory.submit')
    def test_submit(self, mock_submit):
        # check if the submit method is called for every dice
        # with a dice object
        mock_dice = mock.Mock()
        for i in range(7, 14):
            self.lower_block.submit(mock_dice, i)
        calls = [
            call(mock_dice),
        ]
        mock_submit.assert_has_calls(calls=calls)

    @patch('kniffel.models.category.LowerCategory.submit')
    def test_submit_2(self, _mock_submit):
        # check if the submit method is called n times
        # once for each die
        mock_dice = mock.Mock()
        call_count = 0
        for i in range(7, 14):
            self.lower_block.submit(mock_dice, i)
            call_count += 1
        self.assertEqual(7, call_count)

    def test_submit_3(self):
        # check if the exception is raised if index out of range
        mock_dice = mock.Mock()
        self.assertRaises(kniffel.exceptions.InvalidIndexError, self.lower_block.submit, mock_dice, 14)
