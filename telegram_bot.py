import logging
import time

from environs import Env
from google.cloud import dialogflow
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logger = logging.getLogger('Telegram logger')

env = Env()
env.read_env()
UPDATER = Updater(env.str('TELEGRAM_BOT_API'))
DIALOGFLOW_PROJECT_ID = env.str('DIALOGFLOW_PROJECT_ID')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Здравствуйте, {user.username}\\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Данный бот написан в рамках учебного проекта devman.org')


def handle_error(exception):
    logger.exception(f'Бот завершил работу с ошибкой: {exception}', exc_info=True)
    logger.info('Бот будет перезапущен через 30 минут')
    time.sleep(1800)
    logger.info('Бот game of verbs запущен в telegram')


def greet(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text(detect_intent_texts(
            DIALOGFLOW_PROJECT_ID,
            update.effective_user.id,
            update.message.text,
            'ru-RU'))
    except Exception as e:
        handle_error(e)


def main() -> None:
    dispatcher = UPDATER.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, greet))
    telegram_logs_token = env.str('TELEGRAM_LOGS_TOKEN')
    chat_id = env.int('TELEGRAM_CHAT_ID')
    tg_bot_logs = telegram.Bot(token=telegram_logs_token)
    logger.setLevel(logging.INFO)
    telegram_logs_handler = TelegramLogsHandler(
        tg_bot=tg_bot_logs,
        chat_id=chat_id
    )
    logger.addHandler(telegram_logs_handler)
    logger.info('Бот game of verbs запущен в telegram')
    while True:
        try:
            UPDATER.start_polling()
            UPDATER.idle()
        except Exception as e:
            handle_error(e)
            continue


if __name__ == '__main__':
    main()
