import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
import requests

class WikipediaBot:
    def __init__(self, token):
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        self.wikipedia = wikipediaapi.Wikipedia('en', headers={'User-Agent': self.user_agent})
        self.translator = Translator()
        self.updater = Updater(token, use_context=True)
        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(MessageHandler(Filters.text, self.search))

    def start(self, update, context):
        update.message.reply_text('Hello! I am a Wikipedia bot. Ask me to search Wikipedia!')

    def search(self, update, context):
        raw_query = update.message.text
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)
        page = self.wikipedia.page(raw_query)

        if page.exists():
            summary = page.summary[0:5000] 
            translated_summary, _ = self.translator.translate_output(summary, self.get_user_language(update))
            self.send_long_text(update, translated_summary)
        else:
            update.message.reply_text("No results found for that search.")

    def send_long_text(self, update, text):
        chunks = [text[i:i + 3000] for i in range(0, len(text), 3000)]
        for chunk in chunks:
            update.message.reply_text(chunk)

    def get_user_language(self, update):
        user_language = 'en' 
        if update.message.from_user and update.message.from_user.language_code:
            user_language = update.message.from_user.language_code.lower()
        return user_language

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

class Translator:

    def translate_output(self, response, user_lang):
        if user_lang != 'en':
            url = f"https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=en&tl={user_lang}&q={response}"
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

            try:
                request_result = requests.get(url, headers=headers).json()
                response = request_result[0]
            except Exception as e:
                print(f"Error in translate_output: {e}")
                response = response

        return response, user_lang

if __name__ == '__main__':
    bot_token = 'YOUR_TELEGRAM_BOT_API_KEY'
    wiki_bot = WikipediaBot(bot_token)
    wiki_bot.run()
