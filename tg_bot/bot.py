from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes, CallbackQueryHandler
import sqlite3

from tg_bot.config import BOT_TOKEN

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

conn.execute('CREATE TABLE IF NOT EXISTS users(user_tg_id, username, first_name, last_name, full_name, language_code, '
             'is_premium, is_bot, password, role text)')


async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Зарегистрироваться", callback_data="register")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Чтобы зарегистрироваться, нажмите на кнопку ниже ⬇️",
        reply_markup=reply_markup
    )


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = query.from_user

    user_tg_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    full_name = user.full_name
    language_code = user.language_code
    is_premium = user.is_premium
    is_bot = user.is_bot

    cursor.execute("SELECT * FROM users WHERE user_tg_id = ?", (user_tg_id,))
    user = cursor.fetchone()

    if user:
        await query.answer("Вы уже зарегистрированы!")
        await query.edit_message_text( f"Ваш логин: {user[1]}\nВаш пароль: {user[-2]}")
    else:
        cursor.execute("INSERT INTO users (user_tg_id, username, first_name, last_name, full_name, language_code, "
                       "is_premium, is_bot, password, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_tg_id, username, first_name, last_name, full_name, language_code, is_premium,
                        is_bot, '111', 'user'))
        conn.commit()
        await query.answer("Вы успешно зарегистрированы!")
        await query.edit_message_text("Регистрация прошла успешно ✅\n"
                                      f"Ваш логин: {username}\nВаш пароль: 111")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(register))
    application.run_polling()


if __name__ == '__main__':
    main()
