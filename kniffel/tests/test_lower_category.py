# pylint: disable=C
# pylint: disable=protected-access
import json
from unittest import TestCase

from parameterized import parameterized

from kniffel.models.category import Kniffel, FourOfAKind, ThreeOfAKind, FullHouse, SmallStraight, LargeStraight, Chance
from kniffel.models.dice import Dice


class TestThreeOfAKind(TestCase):
    three_of_a_kind_dice = []
    with open('kniffel/tests/dice/three_of_a_kind_dice.json', 'r', encoding="UTF-8") as dice_file:
        three_of_a_kind_dice_numbers = json.load(dice_file)
        for dice in three_of_a_kind_dice_numbers:
            three_of_a_kind_dice.append(Dice(values=dice))
    not_three_of_a_kind_dice = []
    with open('kniffel/tests/dice/not_three_of_a_kind_dice.json', 'r', encoding="UTF-8") as dice_file:
        not_three_of_a_kind_dice_numbers = json.load(dice_file)
        for dice in not_three_of_a_kind_dice_numbers:
            not_three_of_a_kind_dice.append(Dice(values=dice))

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
    four_of_a_kind_dice = []
    with open('kniffel/tests/dice/four_of_a_kind_dice.json', 'r', encoding="UTF-8") as dice_file:
        four_of_a_kind_dice_numbers = json.load(dice_file)
        for dice in four_of_a_kind_dice_numbers:
            four_of_a_kind_dice.append(Dice(values=dice))
    not_four_of_a_kind_dice = []
    with open('kniffel/tests/dice/not_four_of_a_kind_dice.json', 'r', encoding="UTF-8") as dice_file:
        not_four_of_a_kind_dice_numbers = json.load(dice_file)
        for dice in not_four_of_a_kind_dice_numbers:
            not_four_of_a_kind_dice.append(Dice(values=dice))

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
    full_house_dice = []
    with open('kniffel/tests/dice/full_house_dice.json', 'r', encoding="UTF-8") as dice_file:
        full_house_dice_numbers = json.load(dice_file)
        for dice in full_house_dice_numbers:
            full_house_dice.append(Dice(values=dice))
    not_full_house_dice = []
    with open('kniffel/tests/dice/not_full_house_dice.json', 'r', encoding="UTF-8") as dice_file:
        not_full_house_dice_numbers = json.load(dice_file)
        for dice in not_full_house_dice_numbers:
            not_full_house_dice.append(Dice(values=dice))

    def setUp(self):
        self.category = FullHouse(9, "Full house")

    @parameterized.expand((str(test_dice), test_dice, 25) for test_dice in full_house_dice)
    def test_evaluate(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(expected_score, self.category.evaluate())

    @parameterized.expand((str(test_dice), test_dice, 0) for test_dice in not_full_house_dice)
    def test_evaluate_not_full_house(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(expected_score, self.category.evaluate())


class TestSmallStraight(TestCase):
    small_straight_dice = []
    with open('kniffel/tests/dice/small_straight_dice.json', 'r', encoding="UTF-8") as dice_file:
        small_straight_dice_numbers = json.load(dice_file)
        for dice in small_straight_dice_numbers:
            small_straight_dice.append(Dice(values=dice))
    not_small_straight_dice = []
    with open('kniffel/tests/dice/not_small_straight_dice.json', 'r', encoding="UTF-8") as dice_file:
        not_small_straight_dice_numbers = json.load(dice_file)
        for dice in not_small_straight_dice_numbers:
            not_small_straight_dice.append(Dice(values=dice))

    def setUp(self):
        self.category = SmallStraight(10, "Small straight")

    @parameterized.expand((str(test_dice), test_dice, 30) for test_dice in small_straight_dice)
    def test_evaluate(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(expected_score, self.category.evaluate())

    @parameterized.expand((str(test_dice), test_dice, 0) for test_dice in not_small_straight_dice)
    def test_evaluate_not_small_straight(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(expected_score, self.category.evaluate())


class TestLargeStraight(TestCase):
    large_straight_dice = []
    with open('kniffel/tests/dice/large_straight_dice.json', 'r', encoding="UTF-8") as dice_file:
        large_straight_dice_numbers = json.load(dice_file)
        for dice in large_straight_dice_numbers:
            large_straight_dice.append(Dice(values=dice))
    not_large_straight_dice = []
    with open('kniffel/tests/dice/not_large_straight_dice.json', 'r', encoding="UTF-8") as dice_file:
        not_large_straight_dice_numbers = json.load(dice_file)
        for dice in not_large_straight_dice_numbers:
            not_large_straight_dice.append(Dice(values=dice))

    def setUp(self):
        self.category = LargeStraight(11, "Large straight")

    @parameterized.expand((str(test_dice), test_dice, 40) for test_dice in large_straight_dice)
    def test_evaluate(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(expected_score, self.category.evaluate())

    @parameterized.expand((str(test_dice), test_dice, 0) for test_dice in not_large_straight_dice)
    def test_evaluate_not_large_straight(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(expected_score, self.category.evaluate())


class TestKniffel(TestCase):
    kniffel_dice = []
    with open('kniffel/tests/dice/kniffel_dice.json', 'r', encoding="UTF-8") as dice_file:
        kniffel_dice_numbers = json.load(dice_file)
        for dice in kniffel_dice_numbers:
            kniffel_dice.append(Dice(values=dice))
    not_kniffel_dice = []
    with open('kniffel/tests/dice/not_kniffel_dice.json', 'r', encoding="UTF-8") as dice_file:
        not_kniffel_dice_numbers = json.load(dice_file)
        for dice in not_kniffel_dice_numbers:
            not_kniffel_dice.append(Dice(values=dice))

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


class TestChance(TestCase):
    all_dice = []
    with open('kniffel/tests/dice/all_dice.json', 'r', encoding="UTF-8") as dice_file:
        all_dice_numbers = json.load(dice_file)
        for dice in all_dice_numbers:
            all_dice.append(Dice(values=dice))

    def setUp(self):
        self.category = Chance(13, "Chance")

    @parameterized.expand((str(test_dice), test_dice,
                           sum(die.value for die in test_dice.dice)) for test_dice in all_dice)
    def test_evaluate(self, _name, input_dice, expected_score):
        self.category.dice = input_dice
        self.assertEqual(self.category.evaluate(), expected_score)
