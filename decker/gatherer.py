from PIL import Image
import requests
from io import BytesIO

from decker.card import Card


class Gatherer(object):

    base = 'https://api.magicthegathering.io'

    def retrieve(self, name):
        response = requests.get(
            '{}/v1/cards?name="{}"'.format(self.base, name)
        )
        if not response.ok:
            print('Bad response {}'.format(response.status_code))
            return None
        data = response.json()
        cards = data['cards']
        if not cards:
            print('No cards')
            return None
        card = cards[0]
        return card
