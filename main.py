import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") or "PASTE_YOUR_TOKEN_HERE"

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Да, давай", callback_data="start_diag")],
        [InlineKeyboardButton("Не сейчас", callback_data="not_now")]
    ]
    await update.message.reply_text(
        "Привет. Я рядом. Всё, что ты скажешь здесь — это важно. Давай разберёмся, как ты себя чувствуешь на самом деле. Начнём?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
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
        await query.edit_message_text("Что тебе ближе всего прямо сейчас?", reply_markup=InlineKeyboardMarkup(keyboard))
    
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

        if keyboard:
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.edit_message_text(text)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.run_polling()

# Запускаем напрямую (без asyncio.run и run_forever!)
if __name__ == "__main__":
    asyncio.run(main())
