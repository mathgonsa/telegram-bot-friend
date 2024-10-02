import logging

from telegram.ext import Updater

from src.config import config
from src.handler import *


class Bot:

    def __init__(self):
        self.updater = Updater(token=config["bot"]["token"])
        self.dispatcher = self.updater.dispatcher

    def run(self):
        logging.info("Bot started")

        self.dispatcher.add_handler(MessageHandler())

        self.updater.start_polling()
        self.updater.idle()
