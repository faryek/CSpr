import telebot
import os
from dotenv import load_dotenv
from telebot import types
import sqlite3

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

info = bot.get_updates()
print(info)

buttons = types.InlineKeyboardMarkup()


left_button  = types.InlineKeyboardButton("←",      callback_data="None")
page_button  = types.InlineKeyboardButton("1/4",    callback_data="None") 
right_button = types.InlineKeyboardButton("→",      callback_data="None")
buy_button   = types.InlineKeyboardButton("Выбрать", callback_data="None")
buttons.add(left_button, page_button, right_button)
buttons.add(buy_button)

connect = sqlite3.connect("data.db")
cursor = connect.cursor()

page_query = cursor.execute("SELECT 'title', 'desc' FROM Performance")
title, desc = page_query.fetchone()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Добро пожаловать. Я телеграм бот для бронирования билетов навыступления в театре. Используйте /show, чтобы показать список доступных выступлений.')

@bot.message_handler(commands=['show'])
def show_perfs(message):
    msg = f"Название: *{title}*\nОписание: *{description}*"
    bot.send_photo(message.chat.id, caption = msg, reply_markup=buttons)

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    if c.data == 'Button':
        bot.send_message(c.message.chat.id, "Чмоньк чмоньк")











bot.infinity_polling()
