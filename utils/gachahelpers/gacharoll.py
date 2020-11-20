import os
import random
import json


class GachaRoll:
    """
    Class for rolling in gacha
    """
    def __init__(self):
        self.rarities = ['R', 'SR', 'SSR', 'UR']
        self.weights = [50, 30, 15, 5]
        with open('data/json/ur.json') as f:
            self.ur = json.load(f)
        with open('data/json/ssr.json') as f:
            self.ssr = json.load(f)
        with open('data/json/sr.json') as f:
            self.sr = json.load(f)
        with open('data/json/r.json') as f:
            self.r = json.load(f)

    async def gacharoll(self):
        """
        Roll for a character
        """
        selection = random.choices(self.rarities, weights=self.weights, k=1)
        if len(selection) == 1:
            if selection[0] == 'R':
                return random.choice(self.r['characters'])
            elif selection[0] == 'SR':
                return random.choice(self.sr['characters'])
            elif selection[0] == 'SSR':
                return random.choice(self.ssr['characters'])
            elif selection[0] == 'UR':
                return random.choice(self.ur['characters'])
        else:
            return random.choice(self.r['characters'])
