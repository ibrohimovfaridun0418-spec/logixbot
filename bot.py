import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

# TOKEN — Heroku config vars ichida bo'ladi
TOKEN = os.getenv("8586777918:AAHETOeAhp__F3rQCe8Xidi57sFoYaHqOpc")
bot = telebot.TeleBot(TOKEN)

# ADMIN ID
ADMIN_ID = 8394486435
GROUP_ID = -1003414479883   # Sen bergan guruh ID

# Foydalanuvchi vaqtinchalik ma'lumotlari
user_data = {}

# --- ASOSIY MENU ---
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📝 E’lon berish"))
    markup.add(KeyboardButton("❌ Bekor qilish"))
    return markup


# --- /start ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! 😊\nQuyidagi tugmalardan foydalaning:",
        reply_markup=main_menu()
    )


# --- E’lon berishni boshlash ---
@bot.message_handler(func=lambda m: m.text == "📝 E’lon berish")
def start_elon(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"step": 1}

    bot.send_message(chat_id, "🛣 Yo‘nalishni kiriting:")
    

# --- Asosiy jarayon ---
@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get("step") in [1,2,3,4,5])
def elon_steps(message):
    chat_id = message.chat.id
    step = user_data[chat_id]["step"]

    if step == 1:
        user_data[chat_id]["direction"] = message.text
        user_data[chat_id]["step"] = 2
        bot.send_message(chat_id, "📝 Izohni kiriting:")

    elif step == 2:
        user_data[chat_id]["description"] = message.text
        user_data[chat_id]["step"] = 3
        bot.send_message(chat_id, "⚖️ Tona kiriting:")

    elif step == 3:
        user_data[chat_id]["weight"] = message.text
        user_data[chat_id]["step"] = 4
        bot.send_message(chat_id, "📞 Telefon raqam kiriting:")

    elif step == 4:
        user_data[chat_id]["phone"] = message.text
        user_data[chat_id]["step"] = 5
        bot.send_message(chat_id, "👤 Usernameni yozing (masalan: @username):")

    elif step == 5:
        user_data[chat_id]["username"] = message.text

        text = (
            "📦 *Y U K   E’ L O N I*\n\n"
            f"🛣 *Yo‘nalish:* {user_data[chat_id]['direction']}\n\n"
            f"📝 *Izoh:* {user_data[chat_id]['description']}\n\n"
            f"⚖️ *Tona:* {user_data[chat_id]['weight']}\n\n"
            f"📞 *Aloqa:* {user_data[chat_id]['phone']}\n\n"
            f"👤 *Yubordi:* {user_data[chat_id]['username']}"
        )

        # Guruhga yuborish
        bot.send_message(GROUP_ID, text, parse_mode="Markdown")

        # Tasdiqlash
        bot.send_message(chat_id, "✅ E’lon guruhga yuborildi!", reply_markup=main_menu())

        user_data.pop(chat_id)


# --- Bekor qilish ---
@bot.message_handler(func=lambda m: m.text == "❌ Bekor qilish")
def cancel(message):
    chat_id = message.chat.id
    user_data.pop(chat_id, None)
    bot.send_message(chat_id, "❌ Bekor qilindi!", reply_markup=main_menu())


# --- Botni ishga tushirish ---
bot.polling(non_stop=True)