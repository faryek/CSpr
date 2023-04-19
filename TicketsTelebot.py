import telebot
import os
from dotenv import load_dotenv
from telebot import types
import sqlite3

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

info = bot.get_updates()
print(info)


left_button  = types.InlineKeyboardButton("←",      callback_data="None")
page_button  = types.InlineKeyboardButton("1/4",    callback_data="None") 
right_button = types.InlineKeyboardButton("→",      callback_data="None")
buy_button   = types.InlineKeyboardButton("Хочу", callback_data="None")
buttons.add(left_button, page_button, right_button)
buttons.add(buy_button)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Добро пожаловать.', reply_markup=buttons)


@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    if c.data == 'Button':
        bot.send_message(c.message.chat.id, "Чмоньк чмоньк")











bot.infinity_polling()
