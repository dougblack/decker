from copy import deepcopy
from decker.card import Card

class CardCache(object):
    """
    Dumb wrapper over a dictionary.
    """
    def __init__(self):
        self._cache = {}

    def get(self, name):
        hit = self._cache.get(name, None)
        if hit:
            return deepcopy(hit)
        return hit

    def set(self, card):
        self._cache[card.name] = card
