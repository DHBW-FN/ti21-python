# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase

from kniffel.game import UpperCategory, Dice


class TestUpperCategory(TestCase):

    def setUp(self) -> None:
        self.category = UpperCategory(1, "Test", 1)
        self.dummy_dice = Dice(5)
        for i in range(5):
            self.dummy_dice.dice[i].value = i

    def test_submit(self):
        self.category.submit(self.dummy_dice)
        self.assertEqual(self.category.dice, self.dummy_dice)

    def test_evaluate(self):
        self.category.dice = self.dummy_dice
        self.assertEqual(self.category.evaluate(), 1)

    def test_test_evaluate(self):
        self.assertEqual(self.category.test_evaluate(self.dummy_dice), 1)
