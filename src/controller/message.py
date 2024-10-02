import telebot

from src.core.learn import learn
from src.core.reply import generate


def learn_and_reply(message: telebot.types.Message):

    learn(message)

    should_answer = False

    if not should_answer:
        return False, None

    message_reply = generate(message)

    if not message_reply:
        return False, None

    print(message_reply)
    return False, message_reply
