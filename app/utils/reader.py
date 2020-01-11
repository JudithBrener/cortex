from app.proto import cortex_pb2


class Reader:

    def __init__(self, sample_path) -> None:
        self.sample_path = sample_path
        self.__read_sample()

    def __read_sample(self):
        pass

    def get_user(self):
        user = cortex_pb2.User()
        user.user_id = 111
        return user
