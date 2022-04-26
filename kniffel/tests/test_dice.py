# pylint: disable=C
# pylint: disable=protected-access
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized

from kniffel.game import Dice


class TestDice(TestCase):
    def setUp(self) -> None:
        self.dice = Dice()

    @parameterized.expand([
        ("five_fives", Dice(values=[5, 5, 5, 5, 5]), 5, 5),
        ("one_ones", Dice(values=[1, 2, 3, 4, 5]), 1, 1),
        ("zero_sixes", Dice(values=[1, 2, 3, 4, 5]), 6, 0),
        ("three_fours", Dice(values=[4, 4, 4, 5, 5]), 4, 3),
        ("two_fives", Dice(values=[4, 4, 4, 5, 5]), 4, 3)
    ])
    def test_count(self, _name, test_dice, number_to_count, expected_value):
        self.dice = test_dice
        self.assertEqual(expected_value, self.dice.count(number_to_count))

    def test_includes_1(self):
        self.assertEqual(self.dice.includes(0), True)

    def test_includes_2(self):
        for i in range(1, 7, 1):
            self.dice.dice[1].value = i
            self.assertEqual(self.dice.includes(i), True)

    def test_includes_3(self):
        for i in range(1, 7, 1):
            for k in range(5):
                self.dice.dice[k].value = i
            self.assertEqual(self.dice.includes(i), True)

    def test_includes_false_1(self):
        self.assertEqual(self.dice.includes(1), False)

    def test_includes_false_2(self):
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

    def test_save_1(self):
        for i in range(5):
            self.assertEqual(self.dice.dice[i].saved, False)

    def test_save_2(self):
        self.dice.save([1, 2])
        for i in range(2):
            self.assertEqual(self.dice.dice[i].saved, True)

    def test_save_3(self):
        self.dice.save([1, 2])
        for i in range(2, 5):
            self.assertEqual(self.dice.dice[i].saved, False)

    def test_save_4(self):
        self.dice.save([1, 2, 3, 4, 5])
        for i in range(5):
            self.assertEqual(self.dice.dice[i].saved, True)

    def test_un_save_1(self):
        for i in range(5):
            self.dice.dice[i].saved = True
        self.dice.un_save([1])
        self.assertEqual(self.dice.dice[0].saved, False)

    def test_un_save_2(self):
        self.dice.un_save([1, 2, 3, 4, 5])
        for i in range(5):
            self.assertEqual(self.dice.dice[i].saved, False)

    def test_is_rolled(self):
        self.dice.roll()
        self.assertEqual(self.dice.is_rolled(), True)

    def test_is_rolled_false(self):
        self.assertEqual(self.dice.is_rolled(), False)
