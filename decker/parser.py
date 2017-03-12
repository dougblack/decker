import json
import re
from decker.deck import Deck
from decker import stack
from decker.card import Card


class Parser(object):

    re_quantity = re.compile('(\d+) (.*)')

    def __init__(self, lines):
        self.stacks = stacks

    def parse(self):
        deck = Deck()
        for stack, lines in self.stacks.items():
            cards = []
            for line in lines:
                if not line:
                    continue

                quantity_match = self.re_quantity.match(line)
                if quantity_match:
                    count = int(quantity_match.group(1))
                    name = quantity_match.group(2)
                else:
                    count = 1
                    name = line

                deck.cards += [Card(name, stack)] * count
        return deck

if __name__ == '__main__':
    stacks = {
        stack.Commander: [
            'Sliver Overlord'
        ],
        stack.Mainboard: [
            '1 Battering Sliver',
            '1 Blade Sliver',
            '1 Blur Sliver',
            '1 Bonesplitter Sliver',
            '1 Brood Sliver',
            '1 Clot Sliver',
            '1 Crypt Sliver',
            '1 Crystalline Sliver',
            '1 Fury Sliver',
            '1 Gemhide Sliver',
            '1 Harmonic Sliver',
            '1 Lymph Sliver',
            '1 Might Sliver',
            '1 Muscle Sliver',
            '1 Plated Sliver',
            '1 Pulmonic Sliver',
            '1 Quick Sliver',
            '1 Root Sliver',
            '1 Shadow Sliver',
            '1 Sidewinder Sliver',
            '1 Sliver Hive',
            '1 Sliver Hivelord',
            '1 Sliver Legion',
            '1 Sliver Overlord',
            '1 Sliver Queen',
            '1 Spinneret Sliver',
            '1 Spitting Sliver',
            '1 Synapse Sliver',
            '1 Synchronous Sliver',
            '1 Venom Sliver',
            '1 Virulent Sliver',
            '68 Wastes',
            '1 Winged Sliver',
        ]
    }
    parser = Parser(stacks)
    deck = parser.parse()
    print(json.dumps(deck.hydrate(), indent=4))
