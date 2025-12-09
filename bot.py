import telebot
import os

TOKEN = os.getenv("8586777918:AAHRqGlnUR8ljNPLVcAf6Nq3ZzuN8zzAZ0Y")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot ishlayapti! 👋")

bot.polling()