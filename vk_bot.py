import logging
import random
import time

from environs import Env
from google.cloud import dialogflow
import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

logger = logging.getLogger('Telegram logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def reply_message(event, vk_api, answer):
    try:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )
    except Exception as e:
        handle_error(e)


def handle_error(exception):
    logger.exception(f'Бот завершил работу с ошибкой: {exception}', exc_info=True)
    logger.info('Бот будет перезапущен через 30 минут')
    time.sleep(1800)
    logger.info('Бот game of verbs запущен в vk')


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


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
                    if answer:
                        reply_message(event, vk_api, answer)
        except Exception as e:
            handle_error(e)
            continue
