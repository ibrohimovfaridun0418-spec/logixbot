import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

TOKEN = os.getenv("8586777918:AAHETOeAhp__F3rQCe8Xidi57sFoYaHqOpc")  # Heroku uchun token o'zgaruvchi
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8394486435  # Sening admin ID'ing
GROUP_ID = -1003414479883  # Guruh ID

user_data = {}

# --- Asosiy menu ---
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
        "Assalomu alaykum!\nQuyidagilardan birini tanlang:",
        reply_markup=main_menu()
    )


# --- E’lon yozishni boshlash ---
@bot.message_handler(func=lambda m: m.text == "📝 E’lon berish")
def start_elon(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"step": 1}
    bot.send_message(chat_id, "📌 Yo‘nalishni kiriting:")
    

# --- Barcha jarayonlar ---
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    step = user_data[chat_id]["step"]

    # 1 — Yo'nalish
    if step == 1:
        user_data[chat_id]["yonalish"] = message.text
        user_data[chat_id]["step"] = 2
        bot.send_message(chat_id, "📍 Manzilni kiriting:")
        return

    # 2 — Narx
    if step == 2:
        user_data[chat_id]["manzil"] = message.text
        user_data[chat_id]["step"] = 3
        bot.send_message(chat_id, "💰 Narxni kiriting:")
        return

    # 3 — Telefon raqam
    if step == 3:
        user_data[chat_id]["narx"] = message.text
        user_data[chat_id]["step"] = 4
        bot.send_message(chat_id, "📞 Telefon raqamingizni kiriting:")
        return

    # 4 — Yakuniy tasdiq
    if step == 4:
        user_data[chat_id]["telefon"] = message.text

        elon = (
            "📢 *Yangi E’lon!*\n\n"
            f"📌 Yo‘nalish: {user_data[chat_id]['yonalish']}\n"
            f"📍 Manzil: {user_data[chat_id]['manzil']}\n"
            f"💰 Narx: {user_data[chat_id]['narx']}\n"
            f"📞 Telefon: {user_data[chat_id]['telefon']}\n\n"
            "⏳ Admin tasdig‘i kutilmoqda..."
        )

        bot.send_message(chat_id, "Sizning e’lon admin tasdig‘iga yuborildi.")

        # Admin uchun
        bot.send_message(
            ADMIN_ID,
            f"📥 *Yangi e’lon keldi!*\n\n{elon}\n\n"
            "Tasdiqlaysizmi?\n\n"
            "/ok - tasdiqlash\n/cancel - rad etish",
            parse_mode="Markdown"
        )

        user_data[chat_id]["step"] = 0  # to'xtatamiz
        return


# --- Admin tasdiqlasa ---
@bot.message_handler(commands=['ok'])
def admin_ok(message):
    if message.chat.id != ADMIN_ID:
        return
    
    last_user = list(user_data.keys())[-1]
    elon = (
        f"📢 *E’lon!*\n\n"
        f"📌 Yo‘nalish: {user_data[last_user]['yonalish']}\n"
        f"📍 Manzil: {user_data[last_user]['manzil']}\n"
        f"💰 Narx: {user_data[last_user]['narx']}\n"
        f"📞 Telefon: {user_data[last_user]['telefon']}"
    )

    bot.send_message(GROUP_ID, elon, parse_mode="Markdown")
    bot.send_message(ADMIN_ID, "E’lon guruhga yuborildi!")
    

# --- Admin rad etsa ---
@bot.message_handler(commands=['cancel'])
def admin_cancel(message):
    if message.chat.id != ADMIN_ID:
        return

    bot.send_message(ADMIN_ID, "❌ E’lon rad etildi.")


# --- Botni ishga tushirish ---
bot.polling(none_stop=True)