"""
Tool to create test dice files.
"""
import pprint
from collections import Counter

from kniffel.models.dice import Dice

all_dice = []
all_dice_numbers = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    all_dice_numbers.append([i, j, k, l, m])
                    new_dice = Dice(values=[i, j, k, l, m])
                    all_dice.append(new_dice)
with open('dice/all_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(all_dice_numbers))

# collect all dice for three of a kind
three_of_a_kind_dice = []
three_of_a_kind_dice_numbers = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    c = Counter([i, j, k, l, m])
                    if max(c.values()) >= 3:
                        three_of_a_kind_dice_numbers.append([i, j, k, l, m])
                        new_dice = Dice(values=[i, j, k, l, m])
                        three_of_a_kind_dice.append(new_dice)
with open('dice/three_of_a_kind_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(three_of_a_kind_dice_numbers))
not_three_of_a_kind_dice = []
not_three_of_a_kind_dice_numbers = []
for dice in all_dice:
    if dice not in three_of_a_kind_dice:
        not_three_of_a_kind_dice_numbers.append(list(die.value for die in dice.dice))
        not_three_of_a_kind_dice.append(dice)
with open('dice/not_three_of_a_kind_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(not_three_of_a_kind_dice_numbers))

# collect all dice for four of a kind
four_of_a_kind_dice = []
four_of_a_kind_dice_numbers = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    c = Counter([i, j, k, l, m])
                    if max(c.values()) >= 4:
                        four_of_a_kind_dice_numbers.append([i, j, k, l, m])
                        new_dice = Dice(values=[i, j, k, l, m])
                        four_of_a_kind_dice.append(new_dice)
with open('dice/four_of_a_kind_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(four_of_a_kind_dice_numbers))
not_four_of_a_kind_dice = []
not_four_of_a_kind_dice_numbers = []
for dice in all_dice:
    if dice not in four_of_a_kind_dice:
        not_four_of_a_kind_dice_numbers.append(list(die.value for die in dice.dice))
        not_four_of_a_kind_dice.append(dice)
with open('dice/not_four_of_a_kind_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(not_four_of_a_kind_dice_numbers))

# collect all dice for a full house
full_house_dice = []
full_house_dice_numbers = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    c = Counter([i, j, k, l, m])
                    if max(c.values()) == 3 and min(c.values()) == 2:
                        full_house_dice_numbers.append([i, j, k, l, m])
                        new_dice = Dice(values=[i, j, k, l, m])
                        full_house_dice.append(new_dice)
with open('dice/full_house_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(full_house_dice_numbers))
not_full_house_dice = []
not_full_house_dice_numbers = []
for dice in all_dice:
    if dice not in full_house_dice:
        not_full_house_dice_numbers.append(list(die.value for die in dice.dice))
        not_full_house_dice.append(dice)
with open('dice/not_full_house_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(not_full_house_dice_numbers))

# collect all dice for a small straight
small_straight_dice = []
small_straight_dice_numbers = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    c = Counter([i, j, k, l, m])
                    for x in range(1, 4):
                        if c[x] >= 1 and c[x + 1] >= 1 and c[x + 2] >= 1 and c[x + 3] >= 1:
                            small_straight_dice_numbers.append([i, j, k, l, m])
                            new_dice = Dice(values=[i, j, k, l, m])
                            small_straight_dice.append(new_dice)
with open('dice/small_straight_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(small_straight_dice_numbers))
not_small_straight_dice = []
not_small_straight_dice_numbers = []
for dice in all_dice:
    if dice not in small_straight_dice:
        not_small_straight_dice_numbers.append(list(die.value for die in dice.dice))
        not_small_straight_dice.append(dice)
with open('dice/not_small_straight_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(not_small_straight_dice_numbers))

# collect all dice for a large straight
large_straight_dice = []
large_straight_dice_numbers = []
for i in range(1, 7):
    for j in range(1, 7):
        for k in range(1, 7):
            for l in range(1, 7):
                for m in range(1, 7):
                    c = Counter([i, j, k, l, m])
                    for x in range(1, 3):
                        if c[x] >= 1 and c[x + 1] >= 1 and c[x + 2] >= 1 and c[x + 3] >= 1 and c[x + 4] >= 1:
                            large_straight_dice_numbers.append([i, j, k, l, m])
                            new_dice = Dice(values=[i, j, k, l, m])
                            large_straight_dice.append(new_dice)
with open('dice/large_straight_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(large_straight_dice_numbers))
not_large_straight_dice = []
not_large_straight_dice_numbers = []
for dice in all_dice:
    if dice not in large_straight_dice:
        not_large_straight_dice_numbers.append(list(die.value for die in dice.dice))
        not_large_straight_dice.append(dice)
with open('dice/not_large_straight_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(not_large_straight_dice_numbers))

# collect all dice for a kniffel
kniffel_dice = []
kniffel_dice_numbers = []
for i in range(1, 7):
    kniffel_dice_numbers.append([i, i, i, i, i])
    new_dice = Dice(values=[i, i, i, i, i])
    kniffel_dice.append(new_dice)
with open('dice/kniffel_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(kniffel_dice_numbers))
not_kniffel_dice = []
not_kniffel_dice_numbers = []
for dice in all_dice:
    if dice not in kniffel_dice:
        not_kniffel_dice_numbers.append(list(die.value for die in dice.dice))
        not_kniffel_dice.append(dice)
with open('dice/not_kniffel_dice.json', 'w', encoding="UTF-8") as dice_file:
    dice_file.write(pprint.pformat(not_kniffel_dice_numbers))
