from decker import image_from_url


class Card(object):
    """
    Represents a card.

    Cards are responsible for knowing their images and what stack they're
    in.
    """
    def __init__(self, name, stack, image_url=None, text=None, image=None):
        self.name = name
        self.stack = stack
        self.image_url = image_url
        self.text = text
        self._image = image

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
