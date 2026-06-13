import requests
import logging
import os
import telebot

from google.cloud import dialogflow_v2beta1 as dialogflow
from dotenv import load_dotenv
from telebot import types
from send_message_tg import send_message_tg
from environs import env


def main():
    load_dotenv()
    token_google = os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/python_scripts/ChatBot/ChatBot_02/vitalius-project-5a42f95173d3.json'   
    chat_id = env.str("TELEGRAM_CHAT_ID")
    tg_bot_token = env.str('TELEGRAM_BOT_API_KEY')
    bot=telebot.TeleBot(tg_bot_token)
    project_id = env.str('PROJECT_ID')
    session_id = env.str('SESSION_ID')
    text = 'Hi'
    language_code = 'ru'
    send_message_tg(bot, session_id, text, language_code, project_id)


if __name__ == "__main__":
    main()