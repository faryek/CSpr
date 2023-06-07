import telebot
import os
from dotenv import load_dotenv
from telebot import types
import sqlite3
import re

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

info = bot.get_updates()
print(info)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Добро пожаловать, {message.from_user.first_name}. Я телеграм бот для бронирования билетов на выступления в театре. Используйте /show, чтобы показать список доступных выступлений.')

@bot.message_handler(commands=['show'])
def show_perfs(message, id = 1, prev_msg = None):
    
    connect = sqlite3.connect("data.db")
    cursor = connect.cursor()
    
    count = int(cursor.execute("SELECT COUNT(*) FROM Performance WHERE place_config!=-1").fetchone()[0])
    
    page_query = cursor.execute(f"SELECT title, desc FROM Performance WHERE place_config!=-1 AND id = {id}")
    title, desc = page_query.fetchone()

    connect.close()

    buttons = types.InlineKeyboardMarkup()

    left  = id-1 if id != 1 else count
    right = id+1 if id != count else 1

    left_button  = types.InlineKeyboardButton("←",      callback_data=f"to {left}")
    var_button  = types.InlineKeyboardButton(f"{str(id)}/{str(count)}",    callback_data="_") 
    right_button = types.InlineKeyboardButton("→",      callback_data=f"to {right}")
    choose_button   = types.InlineKeyboardButton("Выбрать", callback_data=f"choose {id}")
    buttons.add(left_button, var_button, right_button)
    buttons.add(choose_button)

    msg  = f"Название: {title}\nОписание: "
    msg += f"{desc}\n" if desc != None else 'нет\n'
    
    bot.send_message(message.chat.id, msg, reply_markup=buttons)

    try: bot.delete_message(message.chat.id, prev_msg.id)
    except: pass


def specify_perf(message, id = 1, rp = -1, prev_msg = None):
    
    connect = sqlite3.connect("data.db")
    cursor = connect.cursor()
    
    perf = cursor.execute(f"SELECT title, det_desc, date FROM Performance WHERE place_config!=-1 AND id = {id}")
    title, desc, date_time = perf.fetchone()
    place_config = cursor.execute(f"SELECT * FROM Hall WHERE Hall.id = (SELECT place_config FROM Performance WHERE id = {id})")
    hall = place_config.fetchone()

    connect.close()

    buttons = types.InlineKeyboardMarkup()
    
    hall = list(hall)
    hall.pop(0)

    if rp == -1:
        for i in range(10):
            n = 0
            for j in list(hall[i]):
                if eval(j) == 0:
                    n += 1
            if n != 0:
                buttons.add(types.InlineKeyboardButton(f'Ряд №{i+1} Мест свободно: {n}', callback_data=f'row {i} {id}'))
        buttons.add(types.InlineKeyboardButton('←', callback_data=f'backp {id}'))
    else:
        for i in range(10):
            if eval(list(hall[rp])[i]) == 0:
                buttons.add(types.InlineKeyboardButton(f'Место №{i+1}', callback_data=f'place {rp} {i} {id}'))
            else:
                buttons.add(types.InlineKeyboardButton('Занято', callback_data='_'))
        buttons.add(types.InlineKeyboardButton('←', callback_data=f'backr {id}'))


        

    date = date_time.split(' ')[0]
    time = date_time.split(' ')[1]

    msg  = f"Название: {title}\nОписание: "
    msg += f"{desc}\n" if desc != None else 'нет\n'
    msg += f"Дата выступления: {date.split('-')[2]}.{date.split('-')[1]}.{date.split('-')[0]} Местное время: {time.split(':')[0]}:{time.split(':')[1]}\n"
    if rp == -1:
        msg += "Пожалуйста выберите ряд\n"
    else:
        msg += "Пожалуйста выберите место\n"


    bot.send_message(message.chat.id, msg, reply_markup=buttons)




    
    try: bot.delete_message(message.chat.id, prev_msg.id)
    except: pass

def verify(message, r, p, id):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton('Да', callback_data=f'Yes {r} {p} {id}'), types.InlineKeyboardButton('Нет', callback_data='No'))
    bot.send_message(message.chat.id, f'Вы уверены, что хотите забронировать {p+1} место в {r+1} ряду?', reply_markup=buttons)
    
def booking(message, r, p, id):
    tnum = None
    bot.send_message(message.chat.id, 'Укажите номер вашего телефона')
    if tnum == None:
        @bot.message_handler(regexp='^\\+?[1-9][0-9]{7,14}$')
        def book(message):
            bot.send_message(message.chat.id, 'Бронирование успешно. Мы отправим вам напоминание в день выступления')
            tnum = message.text
    print(tnum)
    
        

@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    if 'to' in c.data:
        id = int(c.data.split(' ')[1])
        show_perfs(c.message, id, prev_msg=c.message)
    elif 'choose' in c.data:
        id = int(c.data.split(' ')[1])
        specify_perf(c.message, id, -1, prev_msg=c.message)
    elif 'row' in c.data:
        rp = int(c.data.split(' ')[1])
        id = int(c.data.split(' ')[2])
        specify_perf(c.message, id, rp, prev_msg=c.message)
    elif 'backp' in c.data:
        id = int(c.data.split(' ')[1])
        show_perfs(c.message, id, prev_msg=c.message)
    elif 'backr' in c.data:
        id = int(c.data.split(' ')[1])
        specify_perf(c.message, id, -1, prev_msg=c.message)
    elif 'place' in c.data:
        r = int(c.data.split(' ')[1])
        p = int(c.data.split(' ')[2])
        id = int(c.data.split(' ')[3])
        verify(c.message, r, p, id)
    elif c.data == 'No':
        try: bot.delete_message(c.message.chat.id, c.message.id)
        except: pass
    elif 'Yes' in c.data:
        r = int(c.data.split(' ')[1])
        p = int(c.data.split(' ')[2])
        id = int(c.data.split(' ')[3])
        booking(c.message, r, p, id)
        try: bot.delete_message(c.message.chat.id, c.message.id)
        except: pass
        
        
        
        












bot.infinity_polling()
