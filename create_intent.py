import json

from google.api_core import exceptions as google_exceptions
from google.cloud import dialogflow_v2beta1 as dialogflow
from dotenv import load_dotenv
from environs import env


def create_intent():
    load_dotenv()
    project_id = env.str('PROJECT_ID')
    with open('intent.json', 'r', encoding='utf-8') as my_file:
        intent_json = my_file.read()
        intent = json.loads(intent_json)
    try:
        for intent_name, intent_item in intent.items():
            if intent_name == 'Устройство на работу':
                display_name = intent_name
                training_phrases_parts = intent_item['questions']
                message_texts = intent_item['answer']
        intents_client = dialogflow.IntentsClient()
        parent = dialogflow.AgentsClient.agent_path(project_id)
        training_phrases = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)
        text = dialogflow.Intent.Message.Text(text=message_texts)
        message = dialogflow.Intent.Message(text=text)
        intent = dialogflow.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message]
        )
        response = intents_client.create_intent(
            request={'parent': parent, "intent": intent}
        )
        print('Intent created: {}'.format(response))
    except google_exceptions.InvalidArgument:
        print('Такой интент уже есть')


if __name__ == "__main__":
    create_intent()
