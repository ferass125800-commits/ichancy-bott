import telebot

TOKEN = '8971500769:AAEK57BL3l9J-w2tzXRtAxO8UufHRKqCCeg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! البوت يعمل الآن بنجاح 🚀")

print("Bot is starting...")
bot.infinity_polling()
