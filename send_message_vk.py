import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from environs import env
from help import get_dialog_response
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType


def echo(event, vk_api, user_id):

    vk_api.messages.send(
        user_id=user_id,
        message=event,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    load_dotenv()
    project_id = env.str('PROJECT_ID')
    session_id = env.str('SESSION_ID')
    language_code = 'ru'
    vk_session = vk.VkApi(token=env.str("VK_API"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            intent = get_dialog_response(session_id, event.text, language_code, project_id)
            if not intent['intent'] == 'Default Fallback Intent':
                echo(intent['response_text'], vk_api, event.user_id)
