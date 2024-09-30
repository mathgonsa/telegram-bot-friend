import telebot

from src.core.learn import learn
from src.core.reply import reply


def learn_and_reply(message: telebot.types.Message):
    print(message)
    learn(message.chat.id, message.text)

    message_reply = reply(message.chat.id, message.text)

    is_to_reply = message_reply is not None
    print("> Reply ", is_to_reply)
    return is_to_reply, message_reply
