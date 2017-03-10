from PIL import Image
from io import BytesIO
import requests


def image_from_url(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image.resize((312, 445))
