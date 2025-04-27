import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# — ВСТАВЬТЕ СВОЙ ТОКЕН —
TOKEN = "7474408171:AAHLvRf85QEXlDIRKO9P-9gbprQ9h2ykoow"

# Дефолтное меню
DEFAULT_IMAGE = "https://i.imgur.com/ogru9Sv.jpeg"
SUPPORT_URL = "https://t.me/broadcastagency"

# Читаем JSON с описаниями
with open("items.json", "r", encoding="utf-8") as f:
    ITEMS = json.load(f)

# Сделать логирование, чтобы видеть ошибки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def build_main_keyboard() -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(item["name"], callback_data=item["callback_data"])] for item in ITEMS]
    kb.append([InlineKeyboardButton("Поддержка", url=SUPPORT_URL)])
    return InlineKeyboardMarkup(kb)

BACK_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="back")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатываем /start — возвращаем главное меню."""
    await update.message.reply_photo(
        photo=DEFAULT_IMAGE,
        caption="""▫️Это мой telegram канал группы\nhttps://t.me/broadcastagency\n
▫️Ссылка на мою группу в instagram\nhttps://www.instagram.com/superstars_.agency?igsh=MWh6OHJyb2d6aDBrNg%3D%3D&utm_source=qr\n
▫️Мой аккаунт для связи в telegram 🔗 @asyax777\n

✨⭐️⭐️⭐️Обращайтесь по любым вопросам и добро пожаловать в нашу команду !⭐️⭐️⭐️✨✨""",
        reply_markup=build_main_keyboard(),
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатываем нажатия inline-кнопок."""
    query = update.callback_query
    await query.answer()  # чтобы кнопка не висела «загрузка»

    data = query.data
    if data == "back":
        # Кнопка «Назад» — возвращаем главное меню
        await query.edit_message_media(
            media=InputMediaPhoto(DEFAULT_IMAGE, caption="""▫️Это мой telegram канал группы\nhttps://t.me/broadcastagency\n
▫️Ссылка на мою группу в instagram\nhttps://www.instagram.com/superstars_.agency?igsh=MWh6OHJyb2d6aDBrNg%3D%3D&utm_source=qr\n
▫️Мой аккаунт для связи в telegram 🔗 @asyax777\n

✨⭐️⭐️⭐️Обращайтесь по любым вопросам и добро пожаловать в нашу команду !⭐️⭐️⭐️✨✨"""),
            reply_markup=build_main_keyboard(),
        )
        return

    # Ищем элемент по callback_data
    item = next((i for i in ITEMS if i["callback_data"] == data), None)
    if not item:
        # Неизвестная кнопка — ничего не делаем
        return

    text = item.get("description", "")
    photo_url = item.get("photo_url")

    if photo_url:
        # Меняем картинку + подпись
        media = InputMediaPhoto(media=photo_url, caption=text)
        await query.edit_message_media(media=media, reply_markup=BACK_MARKUP)
    else:
        # Только меняем подпись под текущим фото
        await query.edit_message_caption(caption=text, reply_markup=BACK_MARKUP)

def main() -> None:
    """Запускаем бота."""
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Запуск в режиме polling
    app.run_polling()

if __name__ == "__main__":
    main()
