from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


# Функція для відправки вітального повідомлення з фоновим зображенням
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Вітаємо! Цей QR-код – не просто лінк, це комплімент від нас і запрошення до знайомства. "
        "Переходь до чат-бота, щоб отримати відповіді на всі твої запитання та дізнатися більше про команду FAVBET. "
        "Тут ми розкриємо все, що тебе цікавить!"
    )

    keyboard = [[InlineKeyboardButton("Почати!", callback_data="main_text")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Відправка зображення як фонового
    with open(r"C:\Users\Ostap\Desktop\TeleBotAcademy\channels4_profile.jpg", "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=InputFile(photo),
            caption=welcome_text,
            reply_markup=reply_markup
        )


# Основний текст із кнопкою переходу до опису позицій
async def main_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.delete_message()  # Видалення попереднього повідомлення з зображенням

    text = (
        "Ми хочемо запросити тебе до команди FAVBET на одну з позицій – Game Presenter (ведучий/ведуча) "
        "або Shuffler (шафлер) для проведення онлайн стрімів."
    )
    keyboard = [[InlineKeyboardButton("Цікавить", callback_data="benefits")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)


# Опис переваг роботи
async def benefits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    text = (
        "Уяви себе у ролі зірки нашої команди — у світі, де кожна твоя фраза додає грі шарму, а кожна дія створює атмосферу. "
        "Ми шукаємо не просто колегу, а того, хто вміє бути на хвилі, відчувати момент і заряджати своєю енергією.\n\n"
        "Майже на місці! Натисни на кнопку, щоб зробити перший крок до команди FAVBET."
    )
    keyboard = [[InlineKeyboardButton("Я готовий(-а)!", callback_data="final")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text, reply_markup=reply_markup)


# Заключний текст із посиланням на рекрутера та зображенням студії
async def final(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    final_text = (
        "Твій інтерес важливий для нас! Просто надішли нашому рекрутеру Владі @vladyslava_hr будь-який емодзі 📨, "
        "щоб дати нам знати, що ти готовий/-а розпочати цю подорож разом із FAVBET! Чекаємо на тебе в нашій команді!"
    )

    with open(r"C:\Users\Ostap\Desktop\TeleBotAcademy\2024-11-04 14.55.24.jpg", "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=InputFile(photo),
            caption=final_text
        )


# Основна функція для запуску бота
def main() -> None:
    application = Application.builder().token("7677813608:AAF6Qj9CidkqWNhkJeKAEOJK4cOfn5FS2ro").build()

    # Додаємо обробник для команди /start
    application.add_handler(CommandHandler("start", start))

    # Додаємо обробники для кнопок
    application.add_handler(CallbackQueryHandler(main_text, pattern="main_text"))
    application.add_handler(CallbackQueryHandler(benefits, pattern="benefits"))
    application.add_handler(CallbackQueryHandler(final, pattern="final"))

    # Запускаємо бота
    application.run_polling()


if __name__ == "__main__":
    main()
