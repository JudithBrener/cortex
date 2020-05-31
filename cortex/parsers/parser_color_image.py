import base64
import json
import pathlib

from PIL import Image

FILE_NAME = 'color_image.jpg'


class ColorImageParser:
    field = 'color_image'

    @staticmethod
    def parse(message):
        message_dict = json.loads(message)
        snapshot = message_dict['snapshot']

        color_image = snapshot['color_image']
        width = color_image['width']
        height = color_image['height']
        data_path = color_image['data_path']
        bin_path = pathlib.Path(data_path)
        img_path = bin_path.parent / FILE_NAME
        with open(bin_path, 'r') as f:
            img_data = f.read()
            img_bytes = base64.b64decode(img_data)
        image = Image.frombytes('RGB', (width, height), img_bytes)
        image.save(img_path)
        result = {'user': message_dict['user'], 'color_image': str(img_path), 'datetime': snapshot['datetime']}
        return json.dumps(result)
