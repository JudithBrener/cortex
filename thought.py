import datetime as dt
import struct


class Thought:
    HEADER_SIZE = 20

    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})'

    def __str__(self):
        return f'[{str(self.timestamp)}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        return isinstance(other, Thought) and self.user_id == other.user_id and \
               self.timestamp == other.timestamp and self.thought == other.thought

    def serialize(self):
        thought = self.thought.encode()
        thought_size = len(thought)
        serialized_thought = struct.pack('<QQI', self.user_id, int(self.timestamp.timestamp()), thought_size)
        serialized_thought += thought
        return serialized_thought

    def deserialize(data):
        user_id, timestamp, thought_size = struct.unpack('<QQI', data[:Thought.HEADER_SIZE])
        datetime = dt.datetime.fromtimestamp(timestamp)
        thought = data[Thought.HEADER_SIZE:].decode()
        return Thought(user_id, datetime, thought)
