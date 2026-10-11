import os
import telebot
from flask import Flask, request

TOKEN = "8971500769:AAG6phF5pWlKR6o8_IFwu2gZrYTcpQtgz7g"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def index():
    return "Bot is active", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
