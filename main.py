import asyncio
import nest_asyncio  # Додаємо цей імпорт
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import os
import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

# Дозволяємо вкладати новий цикл подій
nest_asyncio.apply()  # Цей виклик дозволяє обробляти події одночасно

# Завантаження змінних з .env
load_dotenv()

# Отримання токенів із .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Шлях до бази даних
DB_PATH = os.getenv("DB_PATH", r"C:/Users/Ostap/Desktop/TeleBotAcademy/database.db")

# Ініціалізація бази даних
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Створюємо таблицю, якщо її ще немає
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_activity (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            visited TEXT DEFAULT '0'
    )
    """)

    # Перевірка наявності колонки 'visited' і додавання, якщо її немає
    cursor.execute("PRAGMA table_info(user_activity)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'visited' not in columns:
        cursor.execute("ALTER TABLE user_activity ADD COLUMN visited TEXT DEFAULT '0'")

    conn.commit()
    conn.close()


# Функція для запису активності
def log_activity(user_id: int, full_name: str, visited: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Перевіряємо, чи є користувач в базі
    cursor.execute("SELECT visited FROM user_activity WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if row:
        # Якщо є, оновлюємо статус (замінюємо посилання, якщо натиснув)
        cursor.execute("UPDATE user_activity SET visited = ? WHERE user_id = ?", (visited, user_id))
    else:
        # Якщо немає, додаємо новий запис
        cursor.execute("INSERT INTO user_activity (user_id, full_name, visited) VALUES (?, ?, ?)",
                       (user_id, full_name, visited))

    conn.commit()
    conn.close()


# Експорт даних у файл Excel
def export_to_excel():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_activity")
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(rows, columns=["№", "Повне ім'я", "User ID"])
    df.to_excel("Активність користувачів.xlsx", index=False)


# Функція для відправки вітального повідомлення
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Цей QR-код – це комплімент від нас і запрошення до нашої команди Spinner. "
        "Тисни кнопку та дізнавайся, як стати частиною нашого світу!"
    )
    keyboard = [[InlineKeyboardButton("Далі!", callback_data="main_text")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text,
                                             reply_markup=reply_markup)
    context.user_data["last_message_id"] = message.message_id


# Інші функції для обробки кнопок
async def main_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
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


async def main_tact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    last_message_id = context.user_data.get("last_message_id")
    if last_message_id:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_message_id)
    text = (
        "Уяви себе у ролі зірки нашої команди — у світі, де кожна твоя фраза додає етеру шарму, "
        "а кожна дія створює атмосферу.  Ми шукаємо не просто колегу, "
        "а того, хто вміє бути на хвилі, відчувати момент і заряджати своєю енергією. \n\n"
        "Spinner — новий, але крутий гравець на ринку, і ти можеш стати частиною команди, про яку ще дізнаються. "
        "Ти готовий/-а?"
    )
    keyboard = [[InlineKeyboardButton("Готовий/(-а)", callback_data="final")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
    context.user_data["last_message_id"] = message.message_id


async def final(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    full_name = update.effective_user.full_name

    # Логування персонального ID користувача
    log_activity(user_id, full_name, str(user_id))  # Замість URL записуємо ID користувача

    last_message_id = context.user_data.get("last_message_id")
    if last_message_id:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_message_id)

    final_text = (
        "Твій інтерес важливий для нас! Просто надішли нашому Head of Academy Аліні будь-який емодзі 📨, "
        "щоб дати нам знати, що ти готовий/-а розпочати цю подорож разом із Spinner! "
        "Чекаємо на тебе в нашій команді, де ти дізнаєшся все, що потрібно для яскравого старту!"
    )
    keyboard = [[InlineKeyboardButton("Написати Аліні", url="http://t.me/aavivat")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(r"front.png", "rb") as photo:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(photo), caption=final_text,
                                     reply_markup=reply_markup)


# Утиліта для перегляду активності
def activity_viewer():
    class ActivityViewer:
        def __init__(self, root):
            self.root = root
            self.root.title("Bot Activity Viewer")
            self.root.geometry("600x400")

            # Стилізація
            self.root.config(bg='#800080')  # Фіолетовий фон
            title = tk.Label(root, text="Активність користувачів", font=("Arial", 16, "bold"), fg="white", bg="#800080")
            title.pack(pady=10)

            # Оновлено: вирівняні стовпці
            self.tree = ttk.Treeview(root, columns=("№", "Повне ім'я", "User ID"), show="headings", height=15)
            self.tree.column("№", width=50, anchor="center")
            self.tree.column("Повне ім'я", width=250, anchor="w")
            self.tree.column("User ID", width=300, anchor="w")

            self.tree.heading("№", text="№")
            self.tree.heading("Повне ім'я", text="Повне ім'я")
            self.tree.heading("User ID", text="User ID")

            self.tree.pack(pady=20)

            # Кнопка для експорту в Excel
            export_button = tk.Button(root, text="Експортувати в Excel", command=export_to_excel, bg="#4CAF50", fg="white")
            export_button.pack(pady=10)

            # Кнопка для оновлення даних
            refresh_button = tk.Button(root, text="Оновити дані", command=self.refresh_data, bg="#800080", fg="white")
            refresh_button.pack(pady=10)

            self.refresh_data()

        def refresh_data(self):
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user_activity")
                data = cursor.fetchall()

                for item in self.tree.get_children():
                    self.tree.delete(item)

                for index, (user_id, full_name, visited) in enumerate(data, 1):
                    self.tree.insert("", "end", values=(index, full_name, user_id))  # Виводимо ID користувача

                conn.close()
            except sqlite3.Error as e:
                showerror("Помилка", f"Не вдалося отримати дані з бази даних: {e}")

        def update_data(self):
            self.refresh_data()
            self.root.after(5000, self.update_data)

    root = tk.Tk()
    app = ActivityViewer(root)
    root.mainloop()


# Функція для запуску бота
async def start_bot():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Додавання обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(main_text, pattern="^main_text$"))
    application.add_handler(CallbackQueryHandler(main_tact, pattern="^main_tact$"))
    application.add_handler(CallbackQueryHandler(final, pattern="^final$"))

    # Запуск бота
    await application.run_polling()


# Основна функція
def main():
    # Ініціалізація бази даних
    init_db()

    # Створення і запуск окремого потоку для бота
    threading.Thread(target=asyncio.run, args=(start_bot(),)).start()

    # Запуск утиліти активності
    activity_viewer()


if __name__ == "__main__":
    main()

