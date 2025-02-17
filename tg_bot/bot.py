from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Твой API токен, который ты получил от @BotFather
TOKEN = '7441012240:AAGzlI9z_MaigMXBKX9paqQueGj-NF2h8Cs'


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет, я твой бот!')


def main():
    # Создание апдейтера и диспетчера
    updater = Updater(TOKEN)

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрируем обработчик команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Начинаем получение обновлений
    updater.start_polling()

    # Ожидаем завершения работы
    updater.idle()


if __name__ == '__main__':
    main()
