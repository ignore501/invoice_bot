import logging
from dotenv import load_dotenv
import os

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from excel_file_edit import make_invoice
from vars import questions, reply_keyboard

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid
# all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# начальные кнопки выбора банка
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Реакция на старт - вывод клавиатуры с выбором банка"""
    global data
    data = []
    await update.message.reply_text(
        questions[0],
        reply_markup=markup)


async def add_data(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(data) < 6:
        data.append(update.message.text)
        await update.message.reply_text(questions[len(data)])
    elif len(data) == 6:
        data.append(update.message.text)
        filename = make_invoice(data)
        path = f'C:/PYTHON/invoice_bot/templates/{filename}.xlsx'
        await context.bot.send_document(chat_id=update.effective_chat.id, document=path, reply_markup=markup)


if __name__ == "__main__":

    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    application = Application.builder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    restart_handler = MessageHandler(filters.Regex(r'Начать сначала'), start)
    data_handler = MessageHandler(filters.TEXT, add_data)

    application.add_handler(start_handler)
    application.add_handler(restart_handler)
    application.add_handler(data_handler)

    application.run_polling()
