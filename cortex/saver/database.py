from abc import abstractmethod, ABC


# An abstract database class used by the saver
class Database(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def create_or_update_user(self, user) -> str:
        pass

    @abstractmethod
    def create_or_update_snapshot(self, user_id, timestamp, topic, topic_data) -> str:
        pass

    @staticmethod
    def get_snapshot_key(user_id, timestamp) -> str:
        return str(user_id) + '_' + str(timestamp)
