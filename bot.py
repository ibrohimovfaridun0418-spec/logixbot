import telebot
import os

TOKEN = os.getenv("8586777918:AAHETOeAhp__F3rQCe8Xidi57sFoYaHqOpc")
bot = telebot.TeleBot(TOKEN)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Assalomu alaykum! Yuk e’lon botiga xush kelibsiz.\n\n"
                          "E'lon berish uchun ketma-ket yo'nalish, izoh, tona va telefon raqamni yuboring.")

# ---- E’lon uchun ma’lumotlarni yig‘ish ----
user_data = {}

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id

    # Agar foydalanuvchi hali boshlamagan bo‘lsa
    if chat_id not in user_data:
        user_data[chat_id] = {"step": 1}
        bot.send_message(chat_id, "🛣 *Yo‘nalishni kiriting:*", parse_mode="Markdown")
        return

    step = user_data[chat_id]["step"]

    # STEP 1 — Yo‘nalish
    if step == 1:
        user_data[chat_id]["direction"] = message.text
        user_data[chat_id]["step"] = 2
        bot.send_message(chat_id, "📝 *Izohni kiriting:*", parse_mode="Markdown")
        return

    # STEP 2 — Izoh
    if step == 2:
        user_data[chat_id]["description"] = message.text
        user_data[chat_id]["step"] = 3
        bot.send_message(chat_id, "⚖️ *Tonani kiriting:*", parse_mode="Markdown")
        return

    # STEP 3 — Tona
    if step == 3:
        user_data[chat_id]["weight"] = message.text
        user_data[chat_id]["step"] = 4
        bot.send_message(chat_id, "📞 *Telefon raqamingizni kiriting:*", parse_mode="Markdown")
        return

    # STEP 4 — Telefon
    if step == 4:
        user_data[chat_id]["phone"] = message.text
        username = message.from_user.username or "Noma'lum"

        # Tayyor e’lon
        direction = user_data[chat_id]["direction"]
        description = user_data[chat_id]["description"]
        weight = user_data[chat_id]["weight"]
        phone = user_data[chat_id]["phone"]

        text = f"""
📦 *Y U K   E’ L O N I*

🛣 *Yo‘nalish:*  
{direction}

📝 *Izoh:*  
{description}

⚖️ *Tona:*  
{weight}

📞 *Aloqa:*  
{phone}

👤 *Yubordi:* @{username}
"""

        bot.send_message(chat_id, text, parse_mode="Markdown")

        # Yangi e’lon uchun boshlanishiga qaytarish
        user_data.pop(chat_id)

        bot.send_message(chat_id, "E’lon tayyor! Yana bir e'lon berishingiz mumkin.")

print("🚀 Bot ishga tushdi...")
bot.infinity_polling()