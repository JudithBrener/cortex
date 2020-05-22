from cortex.saver.database import Database


class InMemoryDB(Database):

    def __init__(self) -> None:
        super().__init__()
        self.users = {}
        self.snapshots = {}

    def create_or_update_user(self, user):
        user_id = user["user_id"]
        self.users[user_id] = user
        return user_id

    def create_or_update_snapshot(self, user_id, timestamp, topic, topic_data):
        snapshot_id = self.get_snapshot_key(user_id, timestamp)
        if snapshot_id not in self.snapshots:
            self.snapshots[snapshot_id] = {}
        self.snapshots[snapshot_id][topic] = topic_data
        self.snapshots[snapshot_id]["user_id"] = user_id
        self.snapshots[snapshot_id]["datetime"] = timestamp
        return snapshot_id
