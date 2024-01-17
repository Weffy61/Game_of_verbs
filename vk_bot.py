import logging
import random

from environs import Env
import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from notifications import TelegramLogsHandler, handle_error, detect_intent_texts

logger = logging.getLogger('Telegram logger')


def reply_message(event, vk_api, answer):
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_token = env.str('VK_API_KEY')
    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    telegram_logs_token = env.str('TELEGRAM_LOGS_TOKEN')
    chat_id = env.int('TELEGRAM_CHAT_ID')
    tg_bot_logs = telegram.Bot(token=telegram_logs_token)
    logger.setLevel(logging.INFO)
    telegram_logs_handler = TelegramLogsHandler(
        tg_bot=tg_bot_logs,
        chat_id=chat_id
    )
    logger.addHandler(telegram_logs_handler)
    logger.info('Бот game of verbs запущен в vk')

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    answer = detect_intent_texts(
                        project_id,
                        event.user_id,
                        event.text,
                        'ru-RU'
                    )
                    if not answer.query_result.intent.is_fallback:
                        reply_message(event, vk_api, answer.query_result.fulfillment_text)
        except Exception as e:
            handle_error(e)
            continue
