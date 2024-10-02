from src.config import encoding, redis

from . import BaseRepository


class RedisRepository(BaseRepository):
    def __init__(self, source_name):
        self.redis = redis
        self.source_name = source_name

    def to_int(self, byte, default):
        if byte is None:
            return default

        return int(byte.decode(encoding))
