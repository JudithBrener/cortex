import json

import numpy as np
import pathlib
import matplotlib.pyplot as plt

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


m = '{"user": {"user_id": "42", "username": "Dan Gittik", "birthday": 699746400, "gender": "MALE"}, "snapshot": {' \
    '"datetime": "1575446887339", "pose": {"translation": {"x": 0.4873843491077423, "y": 0.007090016733855009, ' \
    '"z": -1.1306129693984985}, "rotation": {"x": -0.10888676356214629, "y": -0.26755994585035286, ' \
    '"z": -0.021271118915446748, "w": 0.9571326384559261}}, "color_image": {"width": 1920, "height": 1080, ' \
    '"data_path": "C:/Users/Judi/AppData/Local/Temp/pytest-of-Judi/pytest-1/test_real_snapshot0/42' \
    '/1575446887339/color_image.bin"}, "depth_image": {"width": 224, "height": 172, "data_path": ' \
    '"C:/Users/Judi/AppData/Local/Temp/pytest-of-Judi/pytest-1/test_real_snapshot0/42/1575446887339' \
    '/depth_image.bin"}, "feelings": {"hunger": 0.0, "thirst": 0.0, "exhaustion": 0.0, "happiness": 0.0}}} '

DepthImageParser.parse(m)
