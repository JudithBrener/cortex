import logging
import time

import pymongo

from cortex.saver.cortexdao import CortexDao

log = logging.getLogger(__name__)
CORTEX_NAMESPACE = "cortex"


class MongoCortexDao(CortexDao):
    def __init__(self, mongo_client) -> None:
        super().__init__()
        self.wait_mongo(mongo_client)
        self.db = mongo_client[CORTEX_NAMESPACE]
        self.db.users.create_index("user_id", unique=True)
        self.db.snapshots.create_index([("user_id", 1), ("datetime", pymongo.ASCENDING)], unique=True)

    def create_or_update_user(self, user) -> str:
        user_id = user["user_id"]
        query = {"user_id": user_id}
        replacement = {"$set": {"_id": user_id, **user}}
        self.db.users.update_one(query, replacement, upsert=True)
        return user_id

    def create_or_update_snapshot(self, user_id, timestamp, topic, topic_data) -> str:
        query = {"user_id": user_id, "datetime": timestamp}
        snapshot_key = self.get_snapshot_key(user_id, timestamp)
        replacement = {"$set": {"_id": snapshot_key, topic: topic_data}}
        self.db.snapshots.update_one(query, replacement, upsert=True)
        return snapshot_key

    @staticmethod
    def wait_mongo(client):
        timeout = 0.001
        for _ in range(20):
            try:
                client.irkkt.command("ping")
            except pymongo.errors.ServerSelectionTimeoutError:
                log.info("Waiting {} seconds for mongo to start...".format(str(timeout)))
                time.sleep(timeout)
                timeout *= 2
            else:
                return
        else:
            raise RuntimeError("Unable to connect to mongodb")
