import logging
import time

import pymongo

from cortex.saver.database import Database

log = logging.getLogger(__name__)
_NAMESPACE = "thoughts-processor"


class MongoDB(Database):
    def __init__(self, mongo_client) -> None:
        super().__init__()
        self.db = mongo_client[_NAMESPACE]
        self.wait_mongo(mongo_client)

    def create_or_update_user(self, user) -> str:
        user_id = user["user_id"]
        self.db.users.update_one({"user_id": user_id}, {"$set": {**user}}, upsert=True)
        pass

    def create_or_update_snapshot(self, user_id, timestamp, topic, topic_data) -> str:
        self.db.snapshots.update_one(
            {"user_id": user_id, "datetime": timestamp}, {"$set": {topic: topic_data}}, upsert=True)

    @staticmethod
    def wait_mongo(client):
        timeout = 0.001
        for _ in range(20):
            try:
                client.irkkt.command("ping")
            except pymongo.errors.ServerSelectionTimeoutError:
                log.info("waiting {} seconds for mongo to start...".format(str(timeout)))
                time.sleep(timeout)
                timeout *= 2
            else:
                return
        else:
            raise RuntimeError("Unable to connect to mongodb")
