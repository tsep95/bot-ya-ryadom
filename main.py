import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler

TOKEN = os.environ.get("BOT_TOKEN") or "PASTE_YOUR_TOKEN_HERE"

user_states = {}

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Да, давай", callback_data="start_diag")],
        [InlineKeyboardButton("Не сейчас", callback_data="not_now")]
    ]
    update.message.reply_text("Привет. Я рядом. Всё, что ты скажешь здесь — это важно. Давай разберёмся, как ты себя чувствуешь на самом деле. Начнём?", reply_markup=InlineKeyboardMarkup(keyboard))

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id

    if query.data == "start_diag":
        keyboard = [
            [InlineKeyboardButton("Тревога", callback_data="diag_trevoga")],
            [InlineKeyboardButton("Апатия", callback_data="diag_apatia")],
            [InlineKeyboardButton("Злость", callback_data="diag_zlost")],
            [InlineKeyboardButton("Вина", callback_data="diag_vina")],
            [InlineKeyboardButton("Просто плохо", callback_data="diag_prosto")],
            [InlineKeyboardButton("Всё нормально, но чего-то не хватает", callback_data="diag_norma")]
        ]
        query.edit_message_text("Что тебе ближе всего прямо сейчас?", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif query.data.startswith("diag_"):
        state = query.data.split("_")[1]
        user_states[user_id] = state

        if state == "trevoga":
            text = "Ты чувствуешь тревогу. Скажи, это состояние:"
            keyboard = [
                [InlineKeyboardButton("Только сегодня", callback_data="trevoga_1")],
                [InlineKeyboardButton("Несколько дней", callback_data="trevoga_2")],
                [InlineKeyboardButton("Уже давно", callback_data="trevoga_3")]
            ]
        else:
            text = "Спасибо. Эта часть пока в разработке."
            keyboard = []

        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Я пока не понимаю таких сообщений. Нажми /start, чтобы начать.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))
    app.run_polling()

if __name__ == "__main__":
    main()
