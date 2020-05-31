import json
import pathlib

import matplotlib.pyplot as plt
import numpy as np

FILE_NAME = 'depth_image.jpg'


class DepthImageParser:
    field = 'depth_image'

    @staticmethod
    def parse(message):
        message_dict = json.loads(message)
        snapshot = message_dict['snapshot']

        depth_image = snapshot['depth_image']
        width = depth_image['width']
        height = depth_image['height']
        data_path = depth_image['data_path']
        bin_path = pathlib.Path(data_path)
        img_path = bin_path.parent / FILE_NAME
        with open(bin_path, 'r') as f:
            img_data = f.read()
        img_data = json.loads(img_data)  # convert data to array-like object
        img_arr = np.array(img_data).reshape((height, width))
        plt.imsave(img_path, img_arr, cmap='hot')
        result = {'user': message_dict['user'], 'depth_image': str(img_path), 'datetime': snapshot['datetime']}
        return json.dumps(result)
