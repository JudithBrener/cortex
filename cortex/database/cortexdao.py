from abc import abstractmethod, ABC


# An abstract Data Access Object used by the saver
class CortexDao(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def create_or_update_user(self, user) -> str:
        pass

    @abstractmethod
    def create_or_update_snapshot(self, user_id, timestamp, topic, topic_data) -> str:
        pass

    @abstractmethod
    def get_users(self) -> list:
        pass

    @abstractmethod
    def get_user(self, user_id) -> dict:
        pass

    @abstractmethod
    def get_snapshots(self, user_id) -> list:
        pass

    @abstractmethod
    def get_snapshot(self, user_id, snapshot_id) -> dict:
        pass

    @abstractmethod
    def get_snapshot_topic(self, user_id, snapshot_id, topic) -> dict:
        pass

    @staticmethod
    def get_snapshot_key(user_id, timestamp) -> str:
        return str(user_id) + '_' + str(timestamp)
