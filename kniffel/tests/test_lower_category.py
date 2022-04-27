# pylint: disable=C
# pylint: disable=protected-access
from collections import Counter
from unittest import TestCase

from parameterized import parameterized

from kniffel.models.category import Kniffel, FourOfAKind, ThreeOfAKind, FullHouse
from kniffel.models.dice import Dice

# collect all dice
all_dice = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    new_dice = Dice(values=[i, j, k, l, m])
                    all_dice.append(new_dice)

# collect all dice for three of a kind
three_of_a_kind_dice = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    c = Counter([i, j, k, l, m])
                    if max(c.values()) >= 3:
                        new_dice = Dice(values=[i, j, k, l, m])
                        three_of_a_kind_dice.append(new_dice)
not_three_of_a_kind_dice = []
for dice in all_dice:
    if dice not in three_of_a_kind_dice:
        not_three_of_a_kind_dice.append(dice)

# collect all dice for four of a kind
four_of_a_kind_dice = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    c = Counter([i, j, k, l, m])
                    if max(c.values()) >= 4:
                        new_dice = Dice(values=[i, j, k, l, m])
                        four_of_a_kind_dice.append(new_dice)
not_four_of_a_kind_dice = []
for dice in all_dice:
    if dice not in four_of_a_kind_dice:
        not_four_of_a_kind_dice.append(dice)

# collect all dice for a full house
full_house_dice = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    c = Counter([i, j, k, l, m])
                    if max(c.values()) == 3 and min(c.values()) == 2:
                        new_dice = Dice(values=[i, j, k, l, m])
                        full_house_dice.append(new_dice)
not_full_house_dice = []
for dice in all_dice:
    if dice not in full_house_dice:
        not_full_house_dice.append(dice)

# collect all dice for a kniffel
kniffel_dice = []
for i in range(1, 7):
    new_dice = Dice(values=[i, i, i, i, i])
    kniffel_dice.append(new_dice)
not_kniffel_dice = []
for dice in all_dice:
    if dice not in kniffel_dice:
        not_kniffel_dice.append(dice)


class TestThreeOfAKind(TestCase):

    def setUp(self):
        self.category = ThreeOfAKind(7, "Three of a kind")

    @parameterized.expand((str(test_dice), test_dice, sum(test_die.value for test_die in test_dice.dice))
                          for test_dice in three_of_a_kind_dice)
    def test_evaluate(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(self.category.evaluate(), expected_score)

    @parameterized.expand((str(test_dice), test_dice, 0) for test_dice in not_three_of_a_kind_dice)
    def test_evaluate_not_three_of_a_kind(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(expected_score, self.category.evaluate())


class TestFourOfAKind(TestCase):

    def setUp(self) -> None:
        self.category = FourOfAKind(8, "Four of a kind")

    @parameterized.expand((str(test_dice), test_dice, sum(test_die.value for test_die in test_dice.dice))
                          for test_dice in four_of_a_kind_dice)
    def test_evaluate(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(self.category.evaluate(), expected_score)

    @parameterized.expand((str(test_dice), test_dice, 0) for test_dice in not_four_of_a_kind_dice)
    def test_evaluate_not_four_of_a_kind(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(self.category.evaluate(), expected_score)


class TestFullHouse(TestCase):

    def setUp(self):
        self.category = FullHouse(9, "Full house")

    @parameterized.expand((str(test_dice), test_dice, 25) for test_dice in full_house_dice)
    def test_evaluate(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(expected_score, self.category.evaluate())


class TestKniffel(TestCase):
    def setUp(self):
        self.category = Kniffel(12, "Kniffel")

    @parameterized.expand((str(test_dice), test_dice, 50) for test_dice in kniffel_dice)
    def test_evaluate(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(self.category.evaluate(), expected_score)

    @parameterized.expand((str(test_dice), test_dice, 0) for test_dice in not_kniffel_dice)
    def test_evaluate_not_kniffel(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(self.category.evaluate(), expected_score)
