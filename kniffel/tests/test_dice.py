# pylint: disable=C
# pylint: disable=protected-access
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from kniffel.game import Dice


class TestDice(TestCase):
    def setUp(self) -> None:
        self.dice = Dice()

    def test_count(self):
        for i in range(5):
            self.dice.dice[i].value = 1
        self.assertEqual(self.dice.count(1), 5)

        for i in range(5):
            self.dice.dice[i].value = i
        self.assertEqual(self.dice.count(1), 1)
        self.assertEqual(self.dice.count(6), 0)

        self.dice.dice[0].value = 4
        self.dice.dice[1].value = 4
        self.dice.dice[2].value = 4
        self.dice.dice[3].value = 5
        self.dice.dice[4].value = 5
        self.assertEqual(self.dice.count(4), 3)
        self.assertEqual(self.dice.count(5), 2)

    def test_includes(self):
        self.assertEqual(self.dice.includes(0), True)
        for i in range(1, 7, 1):
            self.dice.dice[1].value = i
            self.assertEqual(self.dice.includes(i), True)
        for i in range(1, 7, 1):
            for k in range(5):
                self.dice.dice[k].value = i
            self.assertEqual(self.dice.includes(i), True)

    def test_includes_false(self):
        self.assertEqual(self.dice.includes(1), False)
        for i in range(5):
            self.dice.dice[i].value = 1
        self.assertEqual(self.dice.includes(0), False)

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
        for i in range(5):
            self.assertEqual(self.dice.dice[i].saved, False)
        self.dice.save([1, 2])
        for i in range(2):
            self.assertEqual(self.dice.dice[i].saved, True)
        for i in range(2, 5):
            self.assertEqual(self.dice.dice[i].saved, False)
        self.dice.save([1, 2, 3, 4, 5])
        for i in range(5):
            self.assertEqual(self.dice.dice[i].saved, True)

    def test_un_save(self):
        for i in range(5):
            self.dice.dice[i].saved = True
        self.dice.un_save([1])
        self.assertEqual(self.dice.dice[0].saved, False)
        self.dice.un_save([1, 2, 3, 4, 5])
        for i in range(5):
            self.assertEqual(self.dice.dice[i].saved, False)

    def test_is_rolled(self):
        self.dice.roll()
        self.assertEqual(self.dice.is_rolled(), True)

    def test_is_rolled_false(self):
        self.assertEqual(self.dice.is_rolled(), False)
