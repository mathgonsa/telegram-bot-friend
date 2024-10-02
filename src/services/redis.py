import redis

from src.config import REDIS_DB, REDIS_HOST, REDIS_PORT


class Redis:

    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
        )

    def instance(self):
        return redis.Redis(connection_pool=self.pool)
