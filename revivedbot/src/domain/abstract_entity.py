from abc import ABC


class AbstractEntity(ABC):
    def __init__(self, message):
        self.chat_id = message.chat.id
        self.chat_type = message.chat.type
        self.user_id = message.from_user.id
        self.first_name = message.from_user.first_name
        self.message = message

    def is_private(self):
        return self.message.chat.type == "private"

    def is_editing(self):
        return self.message.edit_date is not None

    def __str__(self):
        return str(self.__dict__)
