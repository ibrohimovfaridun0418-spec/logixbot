import telebot
import os

TOKEN = os.getenv("8586777918:AAHETOeAhp__F3rQCe8Xidi57sFoYaHqOpc")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Yuk e’lon botiga xush kelibsiz!")

@bot.message_handler(func=lambda m: True)
def get_data(message):
    try:
        data = message.text.split('|')

        direction = data[0]
        description = data[1]
        weight = data[2]
        phone = data[3]

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
        bot.send_message(message.chat.id, "❗ Format xato!\n\nMasalan:\nToshkent-Andijon | yuk bor | 3 tonna | +99890xxxxxxx")

bot.polling(non_stop=True)