import os
import telebot
import logging

from dotenv import load_dotenv
from environs import env
from get_dialog_response import get_dialog_response


def send_message_tg(bot, project_id, text=''):
    @bot.message_handler(func=lambda message: message.text in ['start'])
    def start_button_message(message):
        bot.send_message(
            message.chat.id,
            text="Здравствуйте"
        )

    @bot.message_handler()
    def send_message(message):
        response = get_dialog_response(f'tg-{message.from_user.id}', message.text, project_id)
        bot.send_message(message.chat.id, text=response['response_text'])
    bot.infinity_polling()


class MyLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == "__main__":
    load_dotenv()
    project_id = env.str('PROJECT_ID')
    token_google = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    chat_id = env.str("TELEGRAM_CHAT_ID")
    tg_bot_token = env.str('TELEGRAM_BOT_API_KEY')
    bot = telebot.TeleBot(tg_bot_token)
    logger = logging.getLogger('MyLogsHandler')
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler(bot, chat_id))
    try:
        send_message_tg(bot, project_id)
    except Exception:
        logger.exception('Бот упал с ошибкой:')

