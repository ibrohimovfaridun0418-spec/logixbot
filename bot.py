import telebot
import time

# Bot tokeni
TOKEN = "8586777918:AAHRqGlnUR8ljNPLVcAf6Nq3ZzuN8zzAZ0Y"

bot = telebot.TeleBot(TOKEN)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f"Assalomu alaykum {user}!\n\n"
        "🚚 *LogiX Yuk Bot*\n"
        "Yuk ma'lumotini yozing — darrov qabul qilaman."
        "\n\nMisol:\n👉 Andijondan Toshkentga yuk bor"
        "\n👉 Mashina kerak"
        "\n👉 Manzil: Chilonzor"
        "\n👉 Narxi: kelishiladi",
        parse_mode="Markdown"
    )

# Har qanday yuborilgan matnni yuk sifatida qabul qilish
@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.strip()

    # Foydalanuvchiga tasdiqlash
    bot.send_message(
        message.chat.id,
        "✅ *Yuk qabul qilindi!*\nAdminlar ko‘rib chiqadi.\n\n"
        f"📄 *Yuk maʼlumotlari:*\n{text}",
        parse_mode="Markdown"
    )

    # Agar kerak bo‘lsa guruhga yuborish:
    try:
        bot.send_message(
            -1003414479883,  # Siz bergan guruh ID
            f"📦 *Yangi yuk kelib tushdi!*\n\n{text}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print("Guruhga yuborishda xato:", e)

# Botni uzluksiz yuritish
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print("Xatolik:", e)
        time.sleep(3)