import random

from src.config import config
from src.utils import deep_get_attr

from .abstract_entity import AbstractEntity


class Message(AbstractEntity):

    def __init__(self, chance, message):
        super(Message, self).__init__(message)

        self.chance = chance
        self.entities = message.entities
        self.anchors = config.getlist("bot", "anchors")

        if self.has_text():
            self.text = message.text
        else:
            self.text = ""

    def has_text(self):
        return self.message.text is not None and self.message.text.strip() != ""

    def is_sticker(self):
        return self.message.sticker is not None

    def has_entities(self):
        return self.entities is not None

    def has_anchors(self):
        return self.has_text() and any(a in self.message.text.split(" ") for a in self.anchors)

    def is_reply_to_bot(self):
        user_name = deep_get_attr(self.message, "reply_to_message.from_user.username")
        return user_name == config["bot"]["name"]

    def is_random_answer(self):
        return random.randint(0, 100) < self.chance

    def is_large_message(self):
        return len(self.message.text.split()) > 60 and random.randint(0, 100) < 20

    def should_answer(self):
        should = self.has_anchors() or self.is_private() or self.is_reply_to_bot() or self.is_random_answer() or self.is_large_message()
        print("Responder: ", should)
        return should
