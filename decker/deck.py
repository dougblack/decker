from PIL import Image

from decker import image_from_url
from decker.card import Card
from decker.card_cache import CardCache
from decker.gatherer import Gatherer


X_OFFSET = 10
Y_OFFSET = 10
IMAGE_WIDTH = 312
IMAGE_HEIGHT = 445
CARD_WIDTH = IMAGE_WIDTH + 2 * X_OFFSET
CARD_HEIGHT = IMAGE_HEIGHT + 2 * Y_OFFSET
DECK_IMAGE_COLS = 10
DECK_IMAGE_ROWS = 7


class Deck(object):
    def __init__(self, card_names, card_back_url=None, hidden_url=None):
        self.card_names = card_names
        self.gatherer = Gatherer()
        self.hidden_url = hidden_url or 'http://media-hearth.cursecdn.com/attachments/39/665/cardback_1.png'
        self.card_back_url = card_back_url
        self.cards = []
        self._hidden_image = None
        self._card_back_image = None
        self._card_cache = CardCache()

    def hydrate_card(self, name):
        cache_hit = self._card_cache.get(name)
        if cache_hit:
            return cache_hit
        else:
            card_data = self.gatherer.retrieve(name)
            card = Card(card_data['name'], card_data['imageUrl'], card_data.get('text'))
            self._card_cache.set(card)
            return card

    def hydrate(self):
        self.cards = [self.hydrate_card(card) for card in self.card_names]
        return self.cards

    def image(self):
        deck_image = Image.new('RGB', (CARD_WIDTH * 10, CARD_HEIGHT * 7))
        for i, card in enumerate(self.cards):
            deck_num = i // 69
            deck_id = i % 69

            grid_x = deck_id % DECK_IMAGE_COLS
            grid_y = deck_id // DECK_IMAGE_COLS

            real_x = grid_x * CARD_WIDTH + X_OFFSET
            real_y = grid_y * CARD_HEIGHT + Y_OFFSET

            deck_image.paste(card.image, (real_x, real_y))

        top_left_corner = (CARD_WIDTH * (DECK_IMAGE_COLS - 1), CARD_HEIGHT * (DECK_IMAGE_ROWS - 1))
        deck_image.paste(self.hidden_image(), top_left_corner)
        deck_image.save('bar.jpg')

        self._image = deck_image
        return self._image

    def hidden_image(self):
        if self._hidden_image:
            return self._hidden_image
        self._hidden_image = image_from_url(self.hidden_url)
        return self._hidden_image

    def card_back_image(self):
        if self._card_back_image:
            return self._card_back_image
        self._card_back_image = image_from_url(self.card_back_url)
        return self._card_back_image
