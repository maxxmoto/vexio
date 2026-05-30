import os
import sys
import logging
import asyncio
from uuid import uuid4
from datetime import datetime

import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

TOKEN = "8964412503:AAEVNUajV66HteTLH8WuN-oHmquPt9IVDQo"
API_URL = os.environ.get("VEXIO_API_URL", "https://vexio-production-c918.up.railway.app")

NAME, PROJECT, PHONE, PTYPE, DESC, CONFIRM = range(6)

PTYPE_KEYBOARD = [
    ["\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043c\u0430\u0433\u0430\u0437\u0438\u043d", "\u041b\u0435\u043d\u0434\u0438\u043d\u0433"],
    ["Telegram-\u0431\u043e\u0442", "\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435"],
    ["\u0414\u0440\u0443\u0433\u043e\u0435"],
]

def make_keyboard(buttons):
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    img_path = os.path.join(os.path.dirname(__file__), "studio.jpg")
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            await update.message.reply_photo(photo=InputFile(f))
    else:
        for ext in (".png", ".jpeg", ".webp"):
            alt = img_path.replace(".jpg", ext)
            if os.path.exists(alt):
                with open(alt, "rb") as f:
                    await update.message.reply_photo(photo=InputFile(f))
                break
    await update.message.reply_text(
        f"\u041f\u0440\u0438\u0432\u0435\u0442, {user.first_name}! \u270c\ufe0f\n\n"
        f"\u041c\u044b \u2014 <b>Vexio Studio</b> \u2014 \u0441\u0442\u0443\u0434\u0438\u044f "
        f"\u043f\u043e \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0435 \u0441\u0430\u0439\u0442\u043e\u0432 "
        f"\u0438 Telegram-\u0431\u043e\u0442\u043e\u0432.\n\n"
        f"\u0421\u043e\u0437\u0434\u0430\u0451\u043c \u043a\u0440\u0443\u0442\u044b\u0435 "
        f"\u043b\u0435\u043d\u0434\u0438\u043d\u0433\u0438, \u0438\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043c\u0430\u0433\u0430\u0437\u0438\u043d\u044b, "
        f"\u0438\u043d\u0442\u0435\u0440\u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0435 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f "
        f"\u0438 \u0443\u043c\u043d\u044b\u0445 \u0431\u043e\u0442\u043e\u0432 \u0434\u043b\u044f \u0432\u0430\u0448\u0435\u0433\u043e \u0431\u0438\u0437\u043d\u0435\u0441\u0430.\n\n"
        f"\u041d\u0430\u0436\u043c\u0438\u0442\u0435 \u043a\u043d\u043e\u043f\u043a\u0443 \u043d\u0438\u0436\u0435, "
        f"\u0447\u0442\u043e\u0431\u044b \u043e\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443.",
        reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443"]]),
        parse_mode="HTML",
    )
    return NAME

async def name_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443":
        await update.message.reply_text(
            "\u041a\u0430\u043a \u0432\u0430\u0441 \u0437\u043e\u0432\u0443\u0442?",
            reply_markup=ReplyKeyboardRemove(),
        )
        return NAME
    context.user_data["name"] = text.strip()
    await update.message.reply_text("\u041e\u0442\u043b\u0438\u0447\u043d\u043e! \u0422\u0435\u043f\u0435\u0440\u044c \u043d\u0430\u0437\u043e\u0432\u0438\u0442\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u0440\u043e\u0435\u043a\u0442\u0430.")
    return PROJECT

async def project_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["project_name"] = update.message.text.strip()
    await update.message.reply_text(
        "\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430 \u0434\u043b\u044f \u0441\u0432\u044f\u0437\u0438."
    )
    return PHONE

async def phone_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text.strip()
    await update.message.reply_text(
        "\u041a\u0430\u043a\u043e\u0439 \u0442\u0438\u043f \u043f\u0440\u043e\u0435\u043a\u0442\u0430 \u0432\u0430\u0441 \u0438\u043d\u0442\u0435\u0440\u0435\u0441\u0443\u0435\u0442?",
        reply_markup=make_keyboard(PTYPE_KEYBOARD),
    )
    return PTYPE

async def ptype_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ptype"] = update.message.text.strip()
    await update.message.reply_text(
        "\u041e\u043f\u0438\u0448\u0438\u0442\u0435 \u043a\u0440\u0430\u0442\u043a\u043e \u0432\u0430\u0448\u0443 \u0438\u0434\u0435\u044e "
        "\u0438\u043b\u0438 \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u00ab\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c\u00bb.",
        reply_markup=make_keyboard([["\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c"]]),
    )
    return DESC

async def desc_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.strip() != "\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c":
        context.user_data["description"] = update.message.text.strip()
    else:
        context.user_data["description"] = ""
    data = context.user_data
    summary = (
        f"\u2714\ufe0f <b>\u041f\u0440\u043e\u0432\u0435\u0440\u044c\u0442\u0435 \u0434\u0430\u043d\u043d\u044b\u0435:</b>\n\n"
        f"\ud83d\udc64 <b>\u0418\u043c\u044f:</b> {data['name']}\n"
        f"\ud83d\udccb <b>\u041f\u0440\u043e\u0435\u043a\u0442:</b> {data['project_name']}\n"
        f"\ud83d\udcde <b>\u0422\u0435\u043b\u0435\u0444\u043e\u043d:</b> {data['phone']}\n"
        f"\ud83d\udcc1 <b>\u0422\u0438\u043f:</b> {data['ptype']}\n"
        + (f"\ud83d\udcdd <b>\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:</b> {data['description']}" if data['description'] else "")
        + "\n\n\u0412\u0441\u0451 \u0432\u0435\u0440\u043d\u043e?"
    )
    await update.message.reply_text(
        summary,
        reply_markup=make_keyboard([["\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", "\u0417\u0430\u043d\u043e\u0432\u043e"]]),
        parse_mode="HTML",
    )
    return CONFIRM

async def confirm_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.strip() == "\u0417\u0430\u043d\u043e\u0432\u043e":
        context.user_data.clear()
        await update.message.reply_text(
            "\u0414\u0430\u0432\u0430\u0439\u0442\u0435 \u043d\u0430\u0447\u043d\u0451\u043c \u0441\u043d\u0430\u0447\u0430\u043b\u0430. \u041a\u0430\u043a \u0432\u0430\u0441 \u0437\u043e\u0432\u0443\u0442?",
            reply_markup=ReplyKeyboardRemove(),
        )
        return NAME
    data = context.user_data
    payload = {
        "name": data.get("name", ""),
        "projectName": data.get("project_name", ""),
        "phone": data.get("phone", ""),
        "type": data.get("ptype", ""),
        "description": data.get("description", ""),
        "catalog": "no",
        "admin": "no",
        "telegram": "yes",
    }
    msg = await update.message.reply_text("\u23f3 \u041e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u044e \u0437\u0430\u044f\u0432\u043a\u0443...")
    try:
        resp = requests.post(f"{API_URL}/api/submit", json=payload, timeout=15)
        if resp.status_code == 201:
            pid = resp.json().get("project_id", "???")
            await msg.edit_text(
                f"\u2705 <b>\u0417\u0430\u044f\u0432\u043a\u0430 \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0430!</b>\n"
                f"\u041d\u043e\u043c\u0435\u0440: <code>{pid}</code>\n\n"
                f"\u041c\u044b \u0441\u0432\u044f\u0436\u0435\u043c\u0441\u044f \u0441 \u0432\u0430\u043c\u0438 \u0432 \u0431\u043b\u0438\u0436\u0430\u0439\u0448\u0435\u0435 \u0432\u0440\u0435\u043c\u044f.",
                parse_mode="HTML",
                reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443"]]),
            )
        else:
            await msg.edit_text(
                f"\u274c \u041e\u0448\u0438\u0431\u043a\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0430: {resp.status_code}\n"
                f"\u041f\u043e\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u043f\u043e\u0437\u0436\u0435.",
                reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443"]]),
            )
    except requests.RequestException as e:
        await msg.edit_text(
            f"\u274c \u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c: {e}",
            reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443"]]),
        )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "\u0414\u043e \u0441\u0432\u044f\u0437\u0438! \u0415\u0441\u043b\u0438 \u0437\u0430\u0445\u043e\u0442\u0438\u0442\u0435 "
        "\u043f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u044c, \u043d\u0430\u043f\u0438\u0448\u0438\u0442\u0435 /start.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, name_step),
            ],
            PROJECT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, project_step),
            ],
            PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, phone_step),
            ],
            PTYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ptype_step),
            ],
            DESC: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, desc_step),
            ],
            CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_step),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    logger.info("Bot started, polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
