import json


def parse_feelings(message):
    message_dict = json.loads(message)
    snapshot = message_dict['snapshot']
    result = {'user': message_dict['user'], 'feelings': snapshot['feelings'], 'datetime': snapshot['datetime']}
    return json.dumps(result)


parse_feelings.field = "feelings"

m = '{"user": {"user_id": 1234, "username": "test user"}, "snapshot": {"datetime": 1456886665, ' \
    '"pose": {"data": [1, 1]}, "color_image": {"data": [1, 1, 1, 1, 1]}, "depth_image": {"data": [1, 1, 1, 1, 1]}, ' \
    '"feelings": {"data": [1, 1,1,1]}}}'
print(parse_feelings(m))