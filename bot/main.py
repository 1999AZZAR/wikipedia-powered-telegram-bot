# bot/main.py

import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from telegram_helper import start, help_command, search, summary

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

MAX_MESSAGE_LENGTH = 2000

def send_message(update, message):
    chunks = [message[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(message), MAX_MESSAGE_LENGTH)]
    for chunk in chunks:
        update.message.reply_text(chunk)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("search", search))
dispatcher.add_handler(CommandHandler("summary", summary))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, search))

updater.start_polling()

logging.info("The bot has started")
logging.info("The bot is listening for messages")

updater.idle()
