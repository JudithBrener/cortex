import struct
import threading
import time
from pathlib import Path

HEADER_SIZE = 20


class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        has_unpacked_header = False
        full_msg = b""
        data = self.connection.receive(HEADER_SIZE)
        full_msg += data
        while True:
            if not has_unpacked_header:
                user_id, timestamp, thought_size = struct.unpack('<QQI', full_msg[:HEADER_SIZE])
                formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))
                has_unpacked_header = True
            data = self.connection.receive(thought_size)
            full_msg += data
            if has_unpacked_header and len(full_msg) - HEADER_SIZE == thought_size:
                Handler.lock.acquire()
                try:
                    path = Path(self.data_dir) / str(user_id)
                    Path(path).mkdir(mode=0o777, parents=True, exist_ok=True)
                    path = path / str(formatted_time + ".txt")
                    with open(path, mode='a+') as file:
                        if path.stat().st_size > 0:
                            file.write("\n")
                        file.write(full_msg[HEADER_SIZE:].decode())
                    has_unpacked_header = False
                    full_msg = b""
                finally:
                    Handler.lock.release()
            if not data:
                break
        self.connection.close()
