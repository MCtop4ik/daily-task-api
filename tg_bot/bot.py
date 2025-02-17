from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет!')


def main():
    application = Application.builder().token('7441012240:AAGzlI9z_MaigMXBKX9paqQueGj-NF2h8Cs').build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()


if __name__ == '__main__':
    main()
