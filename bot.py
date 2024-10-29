import logging
from dotenv import load_dotenv
import os

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler,
    ContextTypes, MessageHandler,
    filters, CallbackQueryHandler
)
import telegramcalendar
from excel_file_edit import make_invoice
from vars import questions, reply_keyboard, pictures

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
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
        reply_markup=markup)    # Выберите ваш банк


async def calendar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data.append(update.message.text)    # Записываем наименование банка
    # await update.message.reply_photo(photo=pictures[1])
    await update.message.reply_text(
        text=questions[1],  # Введите дату счёта:
        reply_markup=telegramcalendar.create_calendar())  # Создаем календарь


async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await update.effective_chat.send_action(action='typing')
    selected, date = await telegramcalendar.process_calendar_selection(update)
    if selected:    # Дата выбрана
        await update.effective_chat.send_action(action='typing')
        date_string = date.strftime("%d.%m.%Y")
        data.append(date_string)
        await update.callback_query.edit_message_text(
            text="Дата счёта %s" % (date.strftime("%d.%m.%Y")),
            reply_markup=None)
        # Введите наименование организации и юридический адрес:
        await update.effective_chat.send_photo(photo=pictures[2])
        await update.effective_chat.send_message(questions[2])


# Функция для записи всех данных кроме наименовнаия банка
async def add_data(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if 1 < len(data) < 6:
        data.append(update.message.text)    # Записываем данные
        if pictures[len(data)] != '':
            await update.effective_chat.send_photo(photo=pictures[len(data)])
        await update.message.reply_text(questions[len(data)])
    elif len(data) == 6:
        data.append(update.message.text)     # Записываем данные
        filename = make_invoice(data)  # Редактируем файл
        path = f'C:/PYTHON/invoice_bot/templates/{filename}.xlsx'
        # Отправляем готовый файл пользователю
        await update.effective_chat.send_action(action='typing')
        await context.bot.send_document(chat_id=update.effective_chat.id,
                                        document=path, reply_markup=markup)

    else:
        await update.effective_chat.send_message('Произошла ошибка,\
            попробуйте начать сначала')


if __name__ == "__main__":

    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    application = Application.builder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    restart_handler = MessageHandler(filters.Regex(r'Начать сначала'), start)
    data_handler = MessageHandler(filters.TEXT, add_data)
    calendar = MessageHandler(filters.Regex(r'БАНК'), calendar_handler)

    application.add_handler(start_handler)
    application.add_handler(restart_handler)
    application.add_handler(calendar)
    application.add_handler(CallbackQueryHandler(inline_handler))
    application.add_handler(data_handler)

    application.run_polling()
