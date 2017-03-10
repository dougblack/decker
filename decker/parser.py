import re
from decker.deck import Deck


class Parser(object):

    re_quantity = re.compile('(\d+) (.*)')

    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        cards = []
        for line in self.lines:
            if not line:
                continue

            quantity_match = self.re_quantity.match(line)
            if quantity_match:
                count = int(quantity_match.group(1))
                name = quantity_match.group(2)
            else:
                count = 1
                name = line

            cards += [name] * count
        deck = Deck(cards)
        return deck

if __name__ == '__main__':
    lines = [
        '1 Swamp',
        '20 Wrangle',
        'Aetherflux Reservoir'
    ]
    parser = Parser(lines)
    deck = parser.parse()
    deck.hydrate()
    deck.image()
