import telebot

from setup import BOT_TOKEN
from src.controller.message import learn_and_reply

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "Online")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    is_to_reply, message_reply = learn_and_reply(message)
    if is_to_reply:
        bot.reply_to(message, message_reply)


bot.infinity_polling()
