import json
import telebot
import requests
import logging
import os


from environs import env
from dotenv import load_dotenv
from telebot import types


load_dotenv()
token_google = os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vitalius-project-5a42f95173d3"
    
chat_id = env.str("TELEGRAM_CHAT_ID")
tg_bot_token = env.str('TELEGRAM_BOT_API_KEY')
bot=telebot.TeleBot(tg_bot_token)


@bot.message_handler(func=lambda message: message.text in ['start'])
def start_button_message(message):
    bot.send_message(
        message.chat.id,
        text = "Здравствуйте"
    )

@bot.message_handler()
def send_message(message):
    bot.send_message(message.chat.id, text =message.text)

bot.infinity_polling()
