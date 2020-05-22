import json
import logging

log = logging.getLogger(__name__)


class Saver:
    def __init__(self, db) -> None:
        self.db = db
        super().__init__()

    def save(self, topic, message):
        parsed_data = json.loads(message)
        user_info = parsed_data['user']
        timestamp = parsed_data['datetime']
        topic_data = parsed_data[topic]
        user_id = self.db.create_or_update_user(user_info)
        self.db.create_or_update_snapshot(user_id, timestamp, topic, topic_data)
