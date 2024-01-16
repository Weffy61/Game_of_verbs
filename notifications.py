import logging
import time

from google.cloud import dialogflow

logger = logging.getLogger('Telegram logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def handle_error(exception):
    logger.exception(f'Бот завершил работу с ошибкой: {exception}', exc_info=True)
    logger.info('Бот будет перезапущен через 30 минут')
    time.sleep(1800)
    logger.info('Бот game of verbs запущен в vk')


def detect_intent_texts(project_id, session_id, texts, language_code, bot):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if bot == 'tg':
        return response.query_result.fulfillment_text
    else:
        if not response.query_result.intent.is_fallback:
            return response.query_result.fulfillment_text
