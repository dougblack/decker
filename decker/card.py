from decker import image_from_url


class Card(object):
    """
    Represents a card.

    Cards are responsible for knowing their images and what stack they're going
    to be a member of.
    """
    def __init__(self, name, image_url, text=None, image=None):
        self.name = name
        self.image_url = image_url
        self.text = text
        self._image = image
        self._stack = None
        self.image  # greedy load image

    def __repr__(self):
        return '<{} {}>'.format(self.name, self.image_url)

    def __str__(self):
        return '<{} {}>'.format(self.name, self.image_url)

    @property
    def image(self):
        if self._image:
            return self._image
        self._image = image_from_url(self.image_url)
        return self._image
