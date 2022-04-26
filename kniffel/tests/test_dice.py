# pylint: disable=C
# pylint: disable=protected-access
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from kniffel.models.dice import Dice


class TestDice(TestCase):
    def setUp(self) -> None:
        self.dice = Dice()

    def test_count(self):
        for i in range(5):
            self.dice.dice[i].value = 1
        self.assertEqual(self.dice.count(1), 5)

    def test_includes(self):
        self.assertEqual(self.dice.includes(0), True)

    def test_includes_false(self):
        self.assertEqual(self.dice.includes(1), False)

    def test_roll(self):
        self.dice.roll()
        for i in range(5):
            self.assertNotEqual(self.dice.dice[i].value, 0)

    def test_silent_roll(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.dice.silent_roll()
            for i in range(5):
                self.assertNotEqual(self.dice.dice[i].value, 0)
            self.assertEqual(fake_out.getvalue(), '')

    def test_save(self):
        self.dice.save([1, 2, 3, 4, 5])
        for i in range(5):
            self.assertEqual(self.dice.dice[i].saved, True)

    def test_un_save(self):
        for i in range(5):
            self.dice.dice[i].saved = True
        self.dice.un_save([1, 2, 3, 4, 5])
        for i in range(5):
            self.assertEqual(self.dice.dice[i].saved, False)

    def test_is_rolled(self):
        self.dice.roll()
        self.assertEqual(self.dice.is_rolled(), True)

    def test_is_rolled_false(self):
        self.assertEqual(self.dice.is_rolled(), False)
