import os
import sys
import logging
import asyncio
from uuid import uuid4
from datetime import datetime

import httpx
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

TOKEN = "8964412503:AAEVNUajV66HteTLH8WuN-oHmquPt9IVDQo"
API_URL = os.environ.get("VEXIO_API_URL", "https://vexio.up.railway.app")

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
        for ext in (".png", ".jpeg", ".webp", ".jfif"):
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
        f"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435:",
        reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443", "\U0001F4F7 \u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e"], ["\U0001F4E2 \u041a\u0430\u043d\u0430\u043b"]]),
        parse_mode="HTML",
    )
    return NAME

async def name_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443":
        await update.message.reply_text(
            "\u041a\u0430\u043a \u0432\u0430\u0441 \u0437\u043e\u0432\u0443\u0442?",
            reply_markup=ReplyKeyboardRemove(),
        )
        return NAME
    if "\U0001F4F7" in text:
        await portfolio_menu(update, context)
        return ConversationHandler.END
    if "\U0001F4E2" in text:
        await update.message.reply_text(
            "\U0001F4E2 <b>Vexio Studio</b> \u2014 \u043a\u0430\u043d\u0430\u043b \u043e \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0435 \u0438 \u043d\u043e\u0432\u044b\u0445 \u043f\u0440\u043e\u0435\u043a\u0442\u0430\u0445:\n\n"
            "https://t.me/vexiostudiocahnnel",
            reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443", "\U0001F4F7 \u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e"], ["\U0001F4E2 \u041a\u0430\u043d\u0430\u043b"]]),
            parse_mode="HTML",
        )
        return NAME
    context.user_data["name"] = text
    await update.message.reply_text(
        "\u041a\u0430\u043a \u043d\u0430\u0437\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u0432\u0430\u0448 \u043f\u0440\u043e\u0435\u043a\u0442?"
    )
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
        f"\U0001F464 <b>\u0418\u043c\u044f:</b> {data['name']}\n"
        f"\U0001F4CB <b>\u041f\u0440\u043e\u0435\u043a\u0442:</b> {data['project_name']}\n"
        f"\U0001F4DE <b>\u0422\u0435\u043b\u0435\u0444\u043e\u043d:</b> {data['phone']}\n"
        f"\U0001F4C1 <b>\u0422\u0438\u043f:</b> {data['ptype']}\n"
        + (f"\U0001F4DD <b>\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435:</b> {data['description']}" if data['description'] else "")
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
        "telegram_username": update.effective_user.username or "",
    }
    msg = await update.message.reply_text("\U0001F4E6 \u0421\u043e\u0431\u0438\u0440\u0430\u044e \u0437\u0430\u044f\u0432\u043a\u0443...")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{API_URL}/api/submit", json=payload, timeout=15)
        await msg.delete()
        if resp.status_code == 201:
            pid = resp.json().get("project_id", "???")
            await update.message.reply_text(
                f"\u2705 <b>\u0423\u0441\u043f\u0435\u0448\u043d\u043e!</b>\n"
                f"\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440 \u0441\u0432\u044f\u0436\u0435\u0442\u0441\u044f \u0441 \u0412\u0430\u043c\u0438 "
                f"\u0432 \u0431\u043b\u0438\u0436\u0430\u0439\u0448\u0435\u0435 \u0432\u0440\u0435\u043c\u044f.\n\n"
                f"\U0001F310 <b>\u041d\u0430\u0448 \u0441\u0430\u0439\u0442:</b> https://vexio.up.railway.app/\n\n"
                f"\U0001F4B0 <b>\u041d\u0430\u0448 \u0441\u043f\u043e\u043d\u0441\u043e\u0440:</b> "
                f"<a href=\"https://t.me/maxxmoto12RU\">MAXXMOTO</a>\n"
                f"\u043b\u0443\u0447\u0448\u0435\u0435 \u043c\u0435\u0441\u0442\u043e \u0434\u043b\u044f \u043f\u043e\u043a\u0443\u043f\u043a\u0438 \u043c\u043e\u0442\u043e\u0442\u0435\u0445\u043d\u0438\u043a\u0438 \u0438\u0437 \u041a\u0430\u0437\u0430\u0445\u0441\u0442\u0430\u043d\u0430",
                parse_mode="HTML",
                reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443", "\U0001F4F7 \u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e"]]),
            )
        else:
            await update.message.reply_text(
                f"\u274c \u041e\u0448\u0438\u0431\u043a\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0430: {resp.status_code}\n"
                f"\u041f\u043e\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u043f\u043e\u0437\u0436\u0435.",
                reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443", "\U0001F4F7 \u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e"]]),
            )
    except httpx.HTTPError as e:
        await msg.delete()
        await update.message.reply_text(
            f"\u274c \u041e\u0448\u0438\u0431\u043a\u0430 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438: {e}",
            reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443", "\U0001F4F7 \u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e"]]),
        )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "\u0414\u043e \u0441\u0432\u044f\u0437\u0438! \u0415\u0441\u043b\u0438 \u0437\u0430\u0445\u043e\u0442\u0438\u0442\u0435 "
        "\u043f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u044c, \u043d\u0430\u043f\u0438\u0448\u0438\u0442\u0435 /start.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def portfolio_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, msg=None):
    keyboard = [
        [InlineKeyboardButton("\U0001F310 \u0421\u0430\u0439\u0442\u044b", callback_data="pf_sites"),
         InlineKeyboardButton("\U0001F916 \u0411\u043e\u0442\u044b", callback_data="pf_bots")],
        [InlineKeyboardButton("\u2190 \u0412 \u043c\u0435\u043d\u044e", callback_data="pf_back")],
    ]
    text = "\U0001F4F7 <b>\u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e Vexio Studio</b>\n\n\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044e:"
    if update.message:
        if msg:
            await msg.delete()
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif update.callback_query:
        query = update.callback_query
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        await query.answer()


async def portfolio_show(update: Update, context: ContextTypes.DEFAULT_TYPE, category, cat_key="sites", index=0):
    query = update.callback_query
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API_URL}/api/portfolio/{category}", timeout=10)
        if resp.status_code != 200 or not resp.json():
            await query.message.edit_text(
                f"\U0001F50D \u0412 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 \u00ab{category}\u00bb \u043f\u043e\u043a\u0430 \u043d\u0435\u0442 \u043f\u0440\u043e\u0435\u043a\u0442\u043e\u0432.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("\u2190 \u041d\u0430\u0437\u0430\u0434", callback_data="pf_menu")]]),
            )
            await query.answer()
            return
        items = resp.json()
        if index < 0 or index >= len(items):
            index = 0
        item = items[index]
        nav = []
        row = []
        if index > 0:
            row.append(InlineKeyboardButton("\u25C0\ufe0f", callback_data=f"pf_{cat_key}_prev_{index}"))
        row.append(InlineKeyboardButton(f"{index+1}/{len(items)}", callback_data="pf_noop"))
        if index < len(items) - 1:
            row.append(InlineKeyboardButton("\u25B6\ufe0f", callback_data=f"pf_{cat_key}_next_{index}"))
        nav.append(row)
        nav.append([InlineKeyboardButton("\u2190 \u041a \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f\u043c", callback_data="pf_menu")])
        text = f"\U0001F4F7 <b>{item['name']}</b>\n\n{item.get('description', '')}"
        if item.get('link'):
            text += f"\n\n\U0001F517 <a href=\"{item['link']}\">{item['link']}</a>"
        if item.get('image'):
            await query.message.delete()
            await query.message.reply_photo(
                photo=item['image'],
                caption=text,
                reply_markup=InlineKeyboardMarkup(nav),
                parse_mode="HTML",
            )
        else:
            await query.message.edit_text(
                text,
                reply_markup=InlineKeyboardMarkup(nav),
                parse_mode="HTML",
            )
        await query.answer()
    except Exception as e:
        logger.error(f"Portfolio error: {e}")
        await query.message.edit_text(f"\u274c \u041e\u0448\u0438\u0431\u043a\u0430: {e}")
        await query.answer()


async def portfolio_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    if data == "pf_back":
        await query.message.delete()
        user = update.effective_user
        await query.message.reply_text(
            f"\u041f\u0440\u0438\u0432\u0435\u0442, {user.first_name}! \u270c\ufe0f",
            reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443", "\U0001F4F7 \u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e"], ["\U0001F4E2 \u041a\u0430\u043d\u0430\u043b"]]),
        )
        await query.answer()
        return
    if data == "pf_menu":
        await portfolio_menu(update, context)
        return
    parts = data.split("_")
    if len(parts) >= 4:
        _, cat_key, direction, idx = parts[0], parts[1], parts[2], int(parts[3])
        category = "\u0421\u0430\u0439\u0442\u044b" if cat_key == "sites" else "\u0411\u043e\u0442\u044b"
        new_idx = idx + (1 if direction == "next" else -1)
        await portfolio_show(update, context, category, cat_key, new_idx)
    elif len(parts) >= 2 and parts[0] == "pf":
        if parts[1] == "noop":
            await query.answer()
            return
        cat_key = parts[1]
        category = "\u0421\u0430\u0439\u0442\u044b" if cat_key == "sites" else "\u0411\u043e\u0442\u044b"
        await portfolio_show(update, context, category, cat_key)


async def handle_channel_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "\U0001F4E2 <b>Vexio Studio</b> \u2014 \u043a\u0430\u043d\u0430\u043b \u043e \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0435 \u0438 \u043d\u043e\u0432\u044b\u0445 \u043f\u0440\u043e\u0435\u043a\u0442\u0430\u0445:\n\n"
        "https://t.me/vexiostudiocahnnel",
        reply_markup=make_keyboard([["\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443", "\U0001F4F7 \u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e"], ["\U0001F4E2 \u041a\u0430\u043d\u0430\u043b"]]),
        parse_mode="HTML",
    )


async def handle_portfolio_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "\U0001F4F7" in update.message.text:
        await portfolio_menu(update, context)


def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^\u0417\u0430\u043f\u043e\u043b\u043d\u0438\u0442\u044c \u0437\u0430\u044f\u0432\u043a\u0443$"), name_step),
        ],
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

    app.add_handler(CallbackQueryHandler(portfolio_callback, pattern="^pf_"))
    app.add_handler(MessageHandler(filters.Regex("\U0001F4F7"), handle_portfolio_text))
    app.add_handler(MessageHandler(filters.Regex("\U0001F4E2"), handle_channel_text))

    logger.info("Bot started, polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
