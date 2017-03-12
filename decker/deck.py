import sys
import tempfile
import random

from PIL import Image
from collections import defaultdict

from imgurpython import ImgurClient

from decker import image_from_url
from decker.card_cache import CardCache
from decker.gatherer import Gatherer
from decker.transforms import TRANSFORMS


X_OFFSET = 10
Y_OFFSET = 10
IMAGE_WIDTH = 312
IMAGE_HEIGHT = 445
CARD_WIDTH = IMAGE_WIDTH + 2 * X_OFFSET
CARD_HEIGHT = IMAGE_HEIGHT + 2 * Y_OFFSET
DECK_IMAGE_COLS = 10
DECK_IMAGE_ROWS = 7


class Deck(object):
    def __init__(self, card_back_url=None, hidden_url=None):
        self.gatherer = Gatherer()
        self.cards = []
        self.hidden_url = hidden_url or 'http://media-hearth.cursecdn.com/attachments/39/665/cardback_1.png'
        self.card_back_url = card_back_url or 'http://media-hearth.cursecdn.com/attachments/39/665/cardback_1.png'
        self._hidden_image = None
        self._card_back_image = None
        self._card_cache = CardCache()

    def hydrate_card(self, card):
        cache_hit = self._card_cache.get(card.name)
        if cache_hit:
            card = cache_hit
        else:
            card_data = self.gatherer.retrieve(card.name)
            card.name = card_data['name']
            card.image_url = card_data['imageUrl']
            card.text = card_data.get('text')
            self._card_cache.set(card)
            card = card
        return card

    def hydrate(self):
        print('Hydrating cards...')
        self.cards = [self.hydrate_card(card) for card in self.cards]
        image_paths = self.image()
        image_links = self.upload(image_paths)
        return self.json(image_links)

    def image(self):
        print('Stitching deck...')
        deck_images = []
        for i, card in enumerate(self.cards):
            deck_id = i // 69
            card_deck_id = i % 69

            card.json_id = 100 * (1 + deck_id) + card_deck_id
            card.deck_id = deck_id

            grid_x = card_deck_id % X_OFFSET
            grid_y = card_deck_id // Y_OFFSET

            real_x = grid_x * CARD_WIDTH + X_OFFSET
            real_y = grid_y * CARD_HEIGHT + Y_OFFSET

            if deck_id >= len(deck_images):
                deck_images.append(Image.new('RGB', (CARD_WIDTH * 10, CARD_HEIGHT * 7)))

            deck_images[-1].paste(card.image, (real_x, real_y))

        image_files = []

        for i, deck_image in enumerate(deck_images):
            bottom_right = (CARD_WIDTH * (DECK_IMAGE_COLS - 1), CARD_HEIGHT * (DECK_IMAGE_ROWS - 1))
            deck_image.paste(self.hidden_image(), bottom_right)

            file = tempfile.NamedTemporaryFile(delete=False)
            deck_image.save(file.name, 'JPEG')
            image_files.append(file.name)

        return image_files

    def upload(self, image_paths):
        print('Uploading images...')
        client = ImgurClient('bafa0d2c3f6500b', '5f56fbfdbb5fb662b7f9e85668438007897c9c2d')
        image_links = []
        for image_path in image_paths:
            resp = client.upload_from_path(image_path)
            if resp:
                image_links.append(resp['link'])
            else:
                print('Upload failed')
        return image_links

    def json(self, image_links):
        print('Constructing JSON...')
        data = {
            'SaveName': '',
            'GameMode': '',
            'Date': '',
            'Table': '',
            'Sky': '',
            'Note': '',
            'Rules': '',
            'PlayerTurn': '',
            'ObjectStates': []
        }

        for stack, cards in self.stacks.items():
            guid = hex(random.randint(0, (16 ** 6) - 1))[2:]
            object_state = {
                'Name': 'DeckCustom',
                'Nickname': stack,
                'Description': '',
                'Grid': True,
                'Locked': False,
                'SidwaysCard': False,
                'GUID': guid,
                'ColorDiffuse': {
                    'r': 0.71323529,
                    'g': 0.71323529,
                    'b': 0.71323529,
                },
                'DeckIDs': [],
                'ContainedObjects': [],
                'Transform': TRANSFORMS[stack],
                'CustomDeck': {}
            }
            for card in cards:
                object_state['DeckIDs'].append(card.json_id)
                object_state['ContainedObjects'].append(
                    {
                        'Name': 'Card',
                        'Nickname': card.name,
                        'CardID': card.json_id,
                        'Transform': TRANSFORMS[stack]
                    }
                )
                if str(card.deck_id) not in object_state['CustomDeck']:
                    object_state['CustomDeck'][str(card.deck_id + 1)] = {
                        'FaceURL': image_links[card.deck_id],
                        'BackURL': self.card_back_url
                    }
            data['ObjectStates'].append(object_state)
        return data


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

    @property
    def stacks(self):
        result = defaultdict(list)
        for card in self.cards:
            result[card.stack].append(card)
        return result
