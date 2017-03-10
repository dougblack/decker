from PIL import Image
import requests

from decker.gatherer import Gatherer


X_OFFSET = 10
Y_OFFSET = 10
IMAGE_WIDTH = 312
IMAGE_HEIGHT = 445
CARD_WIDTH = IMAGE_WIDTH + 2 * X_OFFSET
CARD_HEIGHT = IMAGE_HEIGHT + 2 * Y_OFFSET


class Deck(object):
    def __init__(self, card_names):
        self.card_names = card_names
        self.gatherer = Gatherer()
        self.cards = []

    def hydrate(self):
        for card in self.card_names:
            new_card = self.gatherer.card(card)
            print(new_card)
            new_card.image()
            self.cards.append(new_card)
        return self.cards

    def image(self):
        deck_image = Image.new('RGB', (CARD_WIDTH * 7, CARD_HEIGHT * 10))
        for i, card in enumerate(self.cards):
            deck_num = i // 69;
            deck_id = i % 69;

            grid_x = deck_id % 10;
            grid_y = deck_id // 10;

            real_x = grid_x * CARD_WIDTH + X_OFFSET;
            real_y = grid_y * CARD_HEIGHT + Y_OFFSET;

            region = (real_x, real_y)
            deck_image.paste(card.image(), region);

        self._image = deck_image
        return self._image
