from src.config import config

from . import RedisRepository


class ChanceRepository(RedisRepository):
    def __init__(self):
        RedisRepository.__init__(self, source_name="chance:{}")
        self.default_chance = config.getint("bot", "default_chance")

    def get(self, chat_id):
        key = self.source_name.format(chat_id)
        chance = self.redis.instance().get(key)

        return self.to_int(chance, self.default_chance)

    def set(self, chat_id, new_chance):

        key = self.source_name.format(chat_id)
        old_chance = self.redis.instance().getset(key, new_chance)

        return self.to_int(old_chance, self.default_chance)
