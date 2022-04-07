# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase

from kniffel.game import Die


class TestDie(TestCase):
    def setUp(self):
        self.die = Die()

    def test_constructor(self):
        self.die = Die(1, True)
        self.assertEqual(self.die.value, 1)
        self.assertTrue(self.die.save)

    def test_all_values_rollable(self):
        rolled_values = [self.die.roll() for _ in range(1000)]
        for value in range(1, 7):
            self.assertIn(value, rolled_values)

    def test_roll(self):
        self.die.value = 0
        self.assertIn(self.die.roll(), range(1, 7))

    def test_save(self):
        self.die.value = 0
        self.die.save()
        self.assertEqual(self.die.roll(), 0)

    def test_un_save(self):
        self.die.saved = True
        self.die.value = 0
        self.die.un_save()
        self.assertIn(self.die.roll(), range(1, 7))
