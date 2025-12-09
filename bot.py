import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

TOKEN = os.getenv("8586777918:AAHETOeAhp__F3rQCe8Xidi57sFoYaHqOpc")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8394486435  # Sening admin ID’ing

user_data = {}

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📝 E’lon berish"))
    markup.add(KeyboardButton("❌ Bekor qilish"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! 😊\nQuyidagi tugmalardan foydalaning:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "📝 E’lon berish")
def start_elon(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"step": 1}
    bot.send_message(chat_id, "🛣 *Yo‘nalishni kiriting:*", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "❌ Bekor qilish")
def cancel(message):
    chat_id = message.chat.id
    if chat_id in user_data:
        del user_data[chat_id]
    bot.send_message(chat_id, "❌ Bekor qilindi!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def handler(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    step = user_data[chat_id]["step"]

    # 1. Yo‘nalish
    if step == 1:
        user_data[chat_id]["direction"] = message.text
        user_data[chat_id]["step"] = 2
        bot.send_message(chat_id, "📝 *Izohni kiriting:*", parse_mode="Markdown")
        return

    # 2. Izoh
    if step == 2:
        user_data[chat_id]["description"] = message.text
        user_data[chat_id]["step"] = 3
        bot.send_message(chat_id, "⚖️ Yuk tonnasini kiriting:", parse_mode="Markdown")
        return

    # 3. Tonna
    if step == 3:
        user_data[chat_id]["weight"] = message.text
        user_data[chat_id]["step"] = 4
        bot.send_message(chat_id, "💵 *Oylik (10 000 so‘mdan kam bo‘lmasin):*", parse_mode="Markdown")
        return

    # 4. Oylik tekshiruv
    if step == 4:
        try:
            pay = int(message.text)
            if pay < 10000:
                bot.send_message(chat_id, "❗ *Oylik 10 000 so‘mdan kam bo‘lmasligi kerak!*", parse_mode="Markdown")
                return
        except:
            bot.send_message(chat_id, "❗ Raqam kiriting!", parse_mode="Markdown")
            return

        user_data[chat_id]["pay"] = message.text
        user_data[chat_id]["step"] = 5
        bot.send_message(chat_id, "📞 Aloqa raqamingizni kiriting:")
        return

    # 5. Aloqa
    if step == 5:
        user_data[chat_id]["phone"] = message.text

        preview = f"""
📦 *Y U K   E’ L O N I*

🛣 *Yo‘nalish:*  
{user_data[chat_id]['direction']}

📝 *Izoh:*  
{user_data[chat_id]['description']}

⚖️ *Tona:*  
{user_data[chat_id]['weight']}

💰 *Oylik:*  
{user_data[chat_id]['pay']} so‘m

📞 *Aloqa:*  
{user_data[chat_id]['phone']}

👤 *Yubordi:* @{message.from_user.username}
"""

        # Userga qaytariladi
        bot.send_message(chat_id, preview, parse_mode="Markdown")
        bot.send_message(chat_id, "📨 E’lon yuborildi!", reply_markup=main_menu())

        # Admin guruhiga/e'lon kanaliga yuboriladi
        bot.send_message(ADMIN_ID, preview, parse_mode="Markdown")

        del user_data[chat_id]
        return

bot.polling(none_stop=True)