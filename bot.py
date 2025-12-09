import telebot
import os

# TOKEN ni Heroku CONFIG VARS dan olish
TOKEN = os.getenv("8586777918:AAHRqGlnUR8ljNPLVcAf6Nq3ZzuN8zzAZ0Y")

if not TOKEN:
    raise ValueError("TOKEN topilmadi! Heroku → Settings → Config Vars → TOKEN qo‘ying.")

bot = telebot.TeleBot(TOKEN)

# /start buyrug‘i
@bot.message_handler(commands=['start'])
def start(msg):
    user = msg.from_user.first_name
    bot.send_message(
        msg.chat.id,
        f"Assalomu alaykum, {user}!\n\n"
        "LogiX botga xush kelibsiz.\n"
        "A'zo bo‘lish uchun quyidagi tugmalardan foydalaning.",
        reply_markup=menu_buttons()
    )

# Asosiy tugmalar
def menu_buttons():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("📥 Guruhga kirish")
    btn2 = telebot.types.KeyboardButton("💳 To'lov qilish")
    btn3 = telebot.types.KeyboardButton("👤 Admin bilan aloqa")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    return markup

# Tugmalarni qayta ishlash
@bot.message_handler(func=lambda m: True)
def handler(msg):
    text = msg.text

    # Guruhga link
    if text == "📥 Guruhga kirish":
        bot.send_message(msg.chat.id, "Guruh: https://t.me/LogiX_grup")

    # To'lov ma’lumotlari
    elif text == "💳 To'lov qilish":
        bot.send_message(
            msg.chat.id,
            "💰 Oylik to‘lov: 10 000 so‘m\n\n"
            "💳 To‘lov kartalari:\n\n"
            "1) Uzcard: 5614 6818 1929 1315\n"
            "   Egasi: I. Faridun\n\n"
            "2) Uzcard: 5614 6835 1590 5578\n"
            "   Egasi: Z. Safarova"
        )

    # Admin kontakt
    elif text == "👤 Admin bilan aloqa":
        bot.send_message(msg.chat.id, "@ibragimov_logist")

    else:
        bot.send_message(msg.chat.id, "Noto‘g‘ri buyruq. Pastdagi tugmalardan foydalaning.")


# Botni ishga tushirish
bot.infinity_polling()