import socket


class Connection:
    def __init__(self, sock):
        self.socket = sock

    def __repr__(self):
        source_ip, source_port = self.socket.getsockname()
        target_ip, target_port = self.socket.getpeername()
        return f'<Connection from {source_ip}:{source_port} to {target_ip}:{target_port}>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def send(self, data):
        self.socket.sendall(data)

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)

    def receive(self, size):
        full_msg = b""
        received_length = 0
        while received_length < size:
            data = self.socket.recv(size - received_length)
            full_msg += data
            received_length = len(full_msg)
            if not data:
                break
        if received_length != size:
            raise Exception
        return full_msg

    def close(self):
        self.socket.close()
