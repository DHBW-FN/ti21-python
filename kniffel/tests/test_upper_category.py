# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase

from kniffel.models.category import UpperCategory
from kniffel.models.dice import Dice


class TestUpperCategory(TestCase):

    def setUp(self) -> None:
        self.category = UpperCategory(1, "Test", 1)
        self.dummy_dice = Dice(5)
        for i in range(5):
            self.dummy_dice.dice[i].value = i

    def test_submit(self):
        self.category.submit(self.dummy_dice)
        self.assertEqual(self.dummy_dice, self.category.dice)

    def test_evaluate(self):
        self.category.dice = self.dummy_dice
        self.assertEqual(1, self.category.evaluate())

    def test_test_evaluate(self):
        self.assertEqual(1, self.category.test_evaluate(self.dummy_dice))
