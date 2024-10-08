import logging
from random import choice

from telegram import ChatAction
from telegram.ext import Filters
from telegram.ext import MessageHandler as ParentHandler
from telegram.ext.dispatcher import run_async

from src.config import config, data_learner, media_checker, reply_generator
from src.domain.message import Message

messages_error = [
    "Chapei de momento e não sei oq responderkkkk",
    "Não respondo viados.",
]


class MessageHandler(ParentHandler):
    def __init__(self):
        super(MessageHandler, self).__init__(Filters.text | Filters.sticker | Filters.photo, self.handle)
        self.data_learner = data_learner
        self.reply_generator = reply_generator
        self.media_checker = media_checker
        self.spam_stickers = config.getlist("bot", "spam_stickers")
        self.media_checker_messages = config.getlist("media_checker", "messages")

    run_async

    def handle(self, bot, update):
        message = Message(chance=25, message=update.message)

        self.__check_media_uniqueness(bot, message)

        if message.has_text() and not message.is_editing():
            self.__process_message(bot, message)

    def __check_media_uniqueness(self, bot, message):
        if not message.is_private() and message.has_entities() and len(message.entities) > 1 and self.media_checker.check(message):
            logging.debug("[Chat %s %s not unique media]" % (message.chat_type, message.chat_id))

            bot.send_message(chat_id=message.chat_id, reply_to_message_id=message.message.message_id, text=choice(self.media_checker_messages))

    def __process_message(self, bot, message):
        logging.info(f"MESSAGE_RECEIVED: {message}")

        should_answer = message.should_answer()

        if should_answer:
            bot.send_chat_action(chat_id=message.chat_id, action=ChatAction.TYPING)

        self.data_learner.learn(message)

        message_answer = None

        if should_answer:
            message_answer = self.reply_generator.generate(message)
            if message_answer is None:
                # text = choice(messages_error)
                pass

        if message_answer:
            reply_id = None if not message.is_reply_to_bot() else message.message.message_id
            bot.send_message(chat_id=message.chat_id, reply_to_message_id=reply_id, text=message_answer)

        logging.info(f"MESSAGE_REPLY: {should_answer} {message_answer}")
        return
