import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.environ.get("BOT_TOKEN") or "PASTE_YOUR_TOKEN_HERE"
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Да, давай", callback_data="start_diag")],
        [InlineKeyboardButton("Пока нет", callback_data="not_now")]
    ]
    await update.message.reply_text(
        "Привет. Я рядом. Всё, что ты скажешь здесь — это важно. Давай попробуем понять, что с тобой происходит. Начнём?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "start_diag":
        keyboard = [
            [InlineKeyboardButton("Я тревожусь и не понимаю, почему", callback_data="state_trevoga")],
            [InlineKeyboardButton("Усталость, будто всё бессмысленно", callback_data="state_apatia")],
            [InlineKeyboardButton("Чувствую раздражение или злость", callback_data="state_zlost")],
            [InlineKeyboardButton("Постоянное чувство вины", callback_data="state_vina")],
            [InlineKeyboardButton("Просто плохо, но не могу объяснить", callback_data="state_prosto")],
            [InlineKeyboardButton("Всё вроде нормально, но чего-то не хватает", callback_data="state_norma")],
        ]
        await query.edit_message_text(
            "Что ближе всего к твоему состоянию прямо сейчас?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    print("Бот запущен и ждёт сообщения...")
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
