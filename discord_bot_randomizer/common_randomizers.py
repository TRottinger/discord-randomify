import random


def flip_coin():
    flip = random.randint(0, 1)
    if flip == 0:
        return 'Heads'
    else:
        return 'Tails'


def roll_dice():
    dice = random.randint(1, 6)
    return dice
