import logging

from environs import Env
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from notifications import TelegramLogsHandler, handle_error, detect_intent_texts

logger = logging.getLogger('Telegram logger')


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Здравствуйте, {user.username}\\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Данный бот написан в рамках учебного проекта devman.org')


def greet(update: Update, context: CallbackContext) -> None:
    dialogflow_project_id = context.bot_data.get('dialogflow_project_id'),
    try:
        update.message.reply_text(detect_intent_texts(
            dialogflow_project_id[0],
            update.effective_user.id,
            update.message.text,
            'ru-RU',
            'tg'))
    except Exception as e:
        handle_error(e)


def main() -> None:
    env = Env()
    env.read_env()
    updater = Updater(env.str('TELEGRAM_BOT_API'))
    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.bot_data['dialogflow_project_id'] = dialogflow_project_id
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
            updater.start_polling()
            updater.idle()
        except Exception as e:
            handle_error(e)
            continue


if __name__ == '__main__':
    main()
