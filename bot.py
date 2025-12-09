import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Assalomu alaykum! Yuk e’lon botiga xush kelibsiz!\n\n"
                     "E’lon yuborish uchun shunday formatda yozing:\n"
                     "Toshkent-Andijon | yuk bor | 3 tonna | +99890xxxxxxx")

@bot.message_handler(func=lambda m: True)
def get_data(message):
    try:
        data = message.text.split('|')

        direction = data[0].strip()
        description = data[1].strip()
        weight = data[2].strip()
        phone = data[3].strip()

        username = message.from_user.username or "no_username"

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

        bot.send_message(message.chat.id, text, parse_mode="Markdown")

    except:
        bot.send_message(message.chat.id,
                         "❗ Format xato!\n\nMasalan:\n"
                         "Toshkent-Andijon | yuk bor | 3 tonna | +99890xxxxxxx")

bot.polling(non_stop=True)