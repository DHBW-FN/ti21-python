# pylint: disable=C
# pylint: disable=protected-access
from unittest import TestCase

from kniffel.models.category import Category
from kniffel.models.dice import Dice
from kniffel.exceptions import CategoryAlreadyFilledError


class TestCategory(TestCase):

    def setUp(self) -> None:
        self.category = Category(index=0, name="Test")

    def test_submit_category_already_filled_error(self):
        self.category.dice = Dice(values=[1, 2, 3, 4, 5])
        self.assertRaises(CategoryAlreadyFilledError, self.category.submit, Dice(values=[1, 2, 3, 4, 5]))

    def test_test_evaluate_already_rolled(self):
        self.category.dice = Dice(values=[1, 2, 3, 4, 5])
        self.assertEqual(-1, self.category.test_evaluate(Dice(values=[1, 2, 3, 4, 5])))
