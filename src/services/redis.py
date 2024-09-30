import redis


class Redis:

    def __init__(self):
        self.pool = redis.ConnectionPool(
            host="localhost",
            port="6379",
            db="0",
        )

    def instance(self):
        return redis.Redis(connection_pool=self.pool)
