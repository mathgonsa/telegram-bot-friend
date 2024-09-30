import telebot

from src.core.learn import learn
from src.core.reply import generate_reply
from src.services.model import generate_reply as model_reply


def learn_and_reply(message: telebot.types.Message):

    learn(message.chat.id, message.text)

    # message_reply = generate_reply(message.chat.id, message.text)
    # if message_reply is None:
    #     return False, message_reply

    message_reply = model_reply(message.text)

    is_to_reply = message_reply is not None

    return is_to_reply, message_reply
