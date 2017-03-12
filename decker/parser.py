import json
import re
from decker.deck import Deck
from decker.stack import Stack
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
        Stack.COMMANDER: [
            'Sliver Overlord'
        ],
        Stack.MAINBOARD: [
            '1 Swamp',
            '70 Wrangle',
        ],
        Stack.SIDEBOARD: [
            '3 Plains',
            'Aetherflux Reservoir',
        ]
    }
    parser = Parser(stacks)
    deck = parser.parse()
    print(json.dumps(deck.hydrate(), indent=4))
