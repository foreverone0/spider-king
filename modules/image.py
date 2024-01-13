from io import BytesIO

from PIL import Image


def read_image_from_bytes(byte_data):
    with BytesIO(byte_data) as img_io:
        image = Image.open(img_io)
        return image


