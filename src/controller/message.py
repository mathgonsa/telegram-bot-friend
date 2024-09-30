import telebot

from src.core.learn import learn
from src.core.reply import generate_reply


def learn_and_reply(message: telebot.types.Message):

    learn(message.chat.id, message.text)

    message_reply = generate_reply(message.chat.id, message.text)
    if message_reply is None:
        return False, message_reply

    is_to_reply = message.message_thread_id

    return is_to_reply, message_reply
