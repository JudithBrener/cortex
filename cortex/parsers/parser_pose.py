import json


def parse_pose(message):
    message_dict = json.loads(message)
    snapshot = message_dict['snapshot']
    result = {'user': message_dict['user'], 'pose': snapshot['pose'], 'datetime': snapshot['datetime']}
    return json.dumps(result)


parse_pose.field = "pose"

