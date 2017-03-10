from PIL import Image
import requests
from io import BytesIO


class Card(object):
    def __init__(self, name, image_url, text=None):
        self.name = name
        self.image_url = image_url
        self.text = text
        self._image = None

    @classmethod
    def from_data(cls, data):
        return cls(data['name'], data['imageUrl'], data.get('text'))

    def __repr__(self):
        return '<{} {}>'.format(self.name, self.image_url)

    def __str__(self):
        return '<{} {}>'.format(self.name, self.image_url)

    def image(self):
        if self._image:
            return self._image
        response = requests.get(self.image_url)
        self._image = Image.open(BytesIO(response.content))
        self._image = self._image.resize((312, 445))
        return self._image
