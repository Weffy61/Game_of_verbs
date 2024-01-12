import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
env = Env()
env.read_env()
UPDATER = Updater(env.str('TELEGRAM_BOT_API'))
DIALOGFLOW_PROJECT_ID = env.str('DIALOGFLOW_PROJECT_ID')


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
    update.message.reply_text('Help!')


def greet(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(detect_intent_texts(
        DIALOGFLOW_PROJECT_ID,
        update.effective_user.id,
        update.message.text,
        'ru-RU'))


def main() -> None:
    try:
        dispatcher = UPDATER.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))

        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, greet))
        UPDATER.start_polling()
        UPDATER.idle()
    except Exception:
        pass


if __name__ == '__main__':
    main()
