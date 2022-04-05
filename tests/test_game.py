# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase

import unittest

from src.game import Dice


class TestDice(TestCase):
    def setUp(self) -> None:
        self.dice = Dice()

    def test_roll(self):
        self.dice.roll()
        for i in range(len(self.dice.dice)):
            self.assertNotEqual(self.dice.dice[i].value, 0)


if __name__ == '__main__':
    unittest.main()
