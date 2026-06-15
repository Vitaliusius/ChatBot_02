import random
import vk_api as vk
import logging
import telebot

from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from environs import env
from get_dialog_response import get_dialog_response
from bot_tg import send_message_tg


def echo(event, vk_api, user_id):
    vk_api.messages.send(
        user_id=user_id,
        message=event,
        random_id=random.randint(1, 1000)
    )


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
    tg_bot_token = env.str('TELEGRAM_BOT_API_KEY')
    bot = telebot.TeleBot(tg_bot_token)
    chat_id = env.str("TELEGRAM_CHAT_ID")
    project_id = env.str('PROJECT_ID')
    session_id = env.str('SESSION_ID')
    logger = logging.getLogger('MyLogsHandler')
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLogsHandler(bot, chat_id))
    try:
        vk_session = vk.VkApi(token=env.str("VK_API"))
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                intent = get_dialog_response(
                    session_id,
                    event.text,
                    project_id
                )
                if not intent['intent'] == 'Default Fallback Intent':
                    echo(
                        intent['response_text'],
                        vk_api,
                        event.user_id
                    )
    except Exception:
        text = logger.exception('Бот vk упал с ошибкой:')
        # send_message_tg(bot, session_id, project_id, text)
        # если раскомментировать, то без vpn будет выдавать ошибку. С vpn приверил - работает.