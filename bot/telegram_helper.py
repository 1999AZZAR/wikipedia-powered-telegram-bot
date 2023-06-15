# bot/telegram_helper.py

from telegram import Update, ChatAction
from telegram.ext import CallbackContext, Updater, MessageHandler, Filters, CommandHandler
from wikipedia_helper import wikipedia_search, wikipedia_summary, wikipedia_url

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    message = f'Hi! I can help you search for information on Wikipedia. Use /help to see the available commands.'
    update.message.reply_text(message)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    help_message = 'Available commands:\n/search <query>\n/summary <title>'
    update.message.reply_text(help_message)

def search(update: Update, context: CallbackContext) -> None:
    """Search for a Wikipedia article."""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    if not context.args:
        update.message.reply_text('Please enter a search query.')
        return
    
    query = ' '.join(context.args)
    results = wikipedia_search(query)
    if not results:
        update.message.reply_text('No results found.')
        return

    # Split the results message into chunks of 1000 characters or less
    result_message = ""
    for i, result in enumerate(results):
        result_chunk = f"{i + 1}. {result['title']}\n{result['url']}\n{result['summary']}\n\n"
        while len(result_chunk) > 0:
            result_message_chunk = result_chunk[:1000]
            result_chunk = result_chunk[1000:]
            update.message.reply_text(result_message_chunk)

def summary(update: Update, context: CallbackContext) -> None:
    """Get the summary of a Wikipedia article."""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    if not context.args:
        update.message.reply_text('Please enter the title of a Wikipedia article.')
        return
    
    title = ' '.join(context.args)
    summary_text = wikipedia_summary(title)
    if not summary_text:
        update.message.reply_text('Article not found.')
        return

    # Split the summary message into chunks of 1000 characters or less
    while len(summary_text) > 0:
        summary_chunk = summary_text[:1000]
        summary_text = summary_text[1000:]
        update.message.reply_text(summary_chunk)
