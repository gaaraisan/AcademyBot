from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

# Завантажуємо змінні з .env
load_dotenv()

# Отримуємо токен з змінних середовища
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Перевірка, чи успішно завантажився токен
if TELEGRAM_TOKEN is None:
    raise ValueError("TELEGRAM_TOKEN не знайдено! Переконайтеся, що він вказаний в .env файлі.")

# Функція для відправки вітального повідомлення з текстом
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Цей QR-код – це комплімент від нас і запрошення до нашої команди Spinner. "
        "Тисни кнопку та дізнавайся, як стати частиною нашого світу!"
    )

    keyboard = [[InlineKeyboardButton("Далі!", callback_data="main_text")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Відправка лише текстового повідомлення без зображення
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_text,
        reply_markup=reply_markup
    )
    # Зберігаємо ID повідомлення для подальшого видалення
    context.user_data["last_message_id"] = message.message_id

# Основний текст із кнопкою переходу до наступного кроку
async def main_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Видалення попереднього повідомлення
    last_message_id = context.user_data.get("last_message_id")
    if last_message_id:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_message_id)

    text = (
        "Ми хочемо запросити тебе приєднатися до команди Spinner на одну з наступних позицій: \n\n"
        "• Game Presenter (ведучий/ведуча) \n\n"
        "• Shuffler (шафлер) \n\n"
        "для проведення онлайн-стрімів."
    )
    keyboard = [[InlineKeyboardButton("Цікаво", callback_data="main_tact")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    context.user_data["last_message_id"] = message.message_id

# Додатковий текст із кнопкою переходу до опису переваг
async def main_tact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Видалення попереднього повідомлення
    last_message_id = context.user_data.get("last_message_id")
    if last_message_id:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_message_id)

    text = (
        "Уяви себе у ролі зірки нашої команди — у світі, де кожна твоя фраза додає етерну шарму, а кожна дія створює атмосферу.  "
        "Ми шукаємо не просто колегу, а того, хто вміє бути на хвилі, відчувати момент і заряджати своєю енергією.\n\n"
        "Spinner — новий, але крутий гравець на ринку, і ти можеш стати "
        "частиною команди, про яку ще дізнаються. Ти готовий/-а?"
    )
    keyboard = [[InlineKeyboardButton("Готовий/(-а)", callback_data="final")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    context.user_data["last_message_id"] = message.message_id

# Заключний текст із посиланням на рекрутера та зображенням студії
async def final(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Видалення попереднього повідомлення
    last_message_id = context.user_data.get("last_message_id")
    if last_message_id:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_message_id)

    final_text = (
        "Твій інтерес важливий для нас! Просто надішли нашому рекрутеру Владі будь-який емодзі 📨, "
        "щоб дати нам знати, що ти готовий/-а розпочати цю подорож разом із Spinner! "
        "Чекаємо на тебе в нашій команді, де ти дізнаєшся все, що потрібно для яскравого старту!"
    )

    # Кнопка з посиланням на профіль рекрутера
    keyboard = [[InlineKeyboardButton("Написати Владі", url="https://t.me/vladyslava_hr")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(r"C:\Users\Ostap\Desktop\TeleBotAcademy\front.png", "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=InputFile(photo),
            caption=final_text,
            reply_markup=reply_markup
        )

# Функція для видалення повідомлень від користувача
async def delete_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.delete()

# Основна функція для запуску бота
def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Додаємо обробник для команди /start із єдиною доступною кнопкою "Почати"
    application.add_handler(CommandHandler("start", start))

    # Додаємо обробники для кнопок
    application.add_handler(CallbackQueryHandler(main_text, pattern="main_text"))
    application.add_handler(CallbackQueryHandler(main_tact, pattern="main_tact"))
    application.add_handler(CallbackQueryHandler(final, pattern="final"))

    # Додаємо обробник для видалення всіх текстових повідомлень
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_user_message))

    # Запускаємо бота
    application.run_polling()

# Перевірка, чи запускається скрипт безпосередньо
if __name__ == "__main__":
    main()
