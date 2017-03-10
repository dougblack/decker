from PIL import Image
import requests
from io import BytesIO

from decker.gatherer import Gatherer


X_OFFSET = 10
Y_OFFSET = 10
IMAGE_WIDTH = 312
IMAGE_HEIGHT = 445
CARD_WIDTH = IMAGE_WIDTH + 2 * X_OFFSET
CARD_HEIGHT = IMAGE_HEIGHT + 2 * Y_OFFSET


class Deck(object):
    def __init__(self, card_names, card_back_url=None, hidden_url=None):
        self.card_names = card_names
        self.gatherer = Gatherer()
        self.hidden_url = hidden_url or 'http://media-hearth.cursecdn.com/attachments/39/665/cardback_1.png'
        self.card_back_url = card_back_url
        self.cards = []
        self._hidden_image = None
        self._card_back_image = None

    def hydrate(self):
        for card in self.card_names:
            new_card = self.gatherer.card(card)
            print(new_card)
            new_card.image()
            self.cards.append(new_card)
        return self.cards

    def image(self):
        deck_image = Image.new('RGB', (CARD_WIDTH * 10, CARD_HEIGHT * 7))
        for i, card in enumerate(self.cards):
            deck_num = i // 69;
            deck_id = i % 69;

            grid_x = deck_id % 10;
            grid_y = deck_id // 10;

            real_x = grid_x * CARD_WIDTH + X_OFFSET;
            real_y = grid_y * CARD_HEIGHT + Y_OFFSET;

            region = (real_x, real_y)
            deck_image.paste(card.image(), region);

        deck_image.paste(self.hidden_image(), (CARD_WIDTH * 9, CARD_HEIGHT * 6))

        self._image = deck_image
        return self._image

    def hidden_image(self):
        if self._hidden_image:
            return self._hidden_image
        response = requests.get(self.hidden_url)
        self._hidden_image = Image.open(BytesIO(response.content))
        self._hidden_image = self._hidden_image.resize((312, 445))
        return self._hidden_image

    def card_back_image(self):
        if self._card_back_image:
            return self._card_back_image
        response = requests.get(self.card_back_url)
        self._card_back_image = Image.open(BytesIO(response.content))
        self._card_back_image = self._card_back_image.resize((312, 445))
        return self._card_back_image
