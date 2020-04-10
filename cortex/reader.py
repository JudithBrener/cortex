import struct
from .proto.cortex_pb2 import User, Snapshot


class Reader:
    def __init__(self, cortex_file):
        self.cortex_file = cortex_file
        self.user = self.read_user()

    def __iter__(self):
        while True:
            snapshot = self.read_snapshot()
            if snapshot is None:
                return
            yield snapshot

    def read_user(self):
        user_size, = struct.unpack('I', self.cortex_file.read(4))
        user = User()
        user.ParseFromString(self.cortex_file.read(user_size))
        return user

    def read_snapshot(self):
        buffer = self.cortex_file.read(4)
        if not buffer:
            return None
        snapshot_size, = struct.unpack('I', buffer)
        snapshot = Snapshot()
        snapshot.ParseFromString(self.cortex_file.read(snapshot_size))
        return snapshot

    # def __iter__(self):
    #     while True:
    #         tell = self.cortex_file.tell()
    #         self.cortex_file.seek(0, 2)  # EOF
    #         if tell == self.cortex_file.tell():
    #             self.cortex_file.close()
    #             return
    #         self.cortex_file.seek(tell)
    #         snapshot = self.read_snapshot()
    #         yield snapshot

    # def read_snapshot(self):
    #     snapshot_size, = struct.unpack('I', self.cortex_file.read(4))
    #     snapshot = Snapshot()
    #     snapshot.ParseFromString(self.cortex_file.read(snapshot_size))
    #     return snapshot
