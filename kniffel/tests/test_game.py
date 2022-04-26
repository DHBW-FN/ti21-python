# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase

import unittest

from kniffel.models.category import ThreeOfAKind
from kniffel.models.dice import Dice


class TestDice(TestCase):
    def setUp(self) -> None:
        self.dice = Dice()

    def test_roll(self):
        self.dice.roll()
        for i in range(len(self.dice.dice)):
            self.assertNotEqual(self.dice.dice[i].value, 0)


class TestCases(TestCase):
    """
    def setUp(self):
        self.category = Category(0, "test")
    """

    def test_ThreeOfAKind(self):
        self.assertGreaterEqual(0, ThreeOfAKind(0, "test").evaluate())


if __name__ == '__main__':
    unittest.main()
