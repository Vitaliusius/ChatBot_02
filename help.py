import requests
import logging
import os
import telebot

from google.cloud import dialogflow_v2beta1 as dialogflow
from dotenv import load_dotenv
from telebot import types
from environs import env


def get_dialog_response(session_id, text, language_code, project_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    dialogflow_response = session_client.detect_intent(session=session, query_input=query_input)
    response = {
        'query_text': dialogflow_response.query_result.query_text,
        'intent': dialogflow_response.query_result.intent.display_name,
        'confidence': dialogflow_response.query_result.intent_detection_confidence,
        'response_text': dialogflow_response.query_result.fulfillment_text,
    }
    return response


def send_message_tg(bot, session_id, text, language_code, project_id):

    @bot.message_handler(func=lambda message: message.text in ['start'])
    def start_button_message(message):
        bot.send_message(
            message.chat.id,
            text = "Здравствуйте"
        )
  
    @bot.message_handler()

    def send_message(message):
        response = get_dialog_response(session_id, message.text, language_code, project_id)
        bot.send_message(message.chat.id, text=response['response_text'])

    bot.infinity_polling()