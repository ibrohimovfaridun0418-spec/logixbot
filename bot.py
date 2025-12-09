import telebot
from telebot import types

TOKEN = "8586777918:AAHRqGlnUR8ljNPLVcAf6Nq3ZzuN8zzAZ0Y"
GROUP_ID = -1003414479883  # Siz aytgan guruh ID

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum, {user}! 👋\nIsmingizni yozib qoldiring."
    )

@bot.message_handler(func=lambda message: True)
def forward_to_group(message):
    try:
        text = f"Yangi xabar:\n\n👤 {message.from_user.first_name}\n💬 {message.text}"
        bot.send_message(GROUP_ID, text)
        bot.reply_to(message, "Xabaringiz guruhga yuborildi! ✅")
    except Exception as e:
        bot.reply_to(message, f"Xatolik: {e}")

bot.polling(none_stop=True)