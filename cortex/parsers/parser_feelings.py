import json


def parse_feelings(message):
    message_dict = json.loads(message)
    snapshot = message_dict['snapshot']
    result = {'user': message_dict['user'], 'feelings': snapshot['feelings'], 'datetime': snapshot['datetime']}
    return json.dumps(result)


parse_feelings.field = "feelings"
