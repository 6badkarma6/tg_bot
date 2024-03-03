#!/usr/bin
import telebot
from telebot import types

from exel import rw

bot = telebot.TeleBot('6788562469:AAFvF-l8F9cJrUJeYSyCsLdnPR7TbyyqbS8')


@bot.message_handler(commands=['start'])
def start(message):
    print('User ' + str(message.from_user.id))
    c1 = types.BotCommand(command='start', description='Start the Bot')
    c2 = types.BotCommand(command='gr1', description='Расписание ПО-1')
    c3 = types.BotCommand(command='gr2', description='Расписание ЭС-2')
    bot.set_my_commands([c1, c2, c3])
    markup = types.InlineKeyboardMarkup()
    #
    # markup.add(types.InlineKeyboardButton("Расписание ПО-1", callback_data='study-po-1'))
    #
    # markup.add(types.InlineKeyboardButton("Расписание ЭС-2", callback_data='study-es-2'))
    #
    bot.send_message(message.from_user.id, ' Bot v0.2b \n Работает с 15:00 по 21:00', reply_markup=markup)


'''@bot.callback_query_handler(func=lambda callback: True)
def study(callback):
    if callback.data == 'study-es-2':
    with open('user.txt', 'a') as file:
        file.write(callback.message.from_user.id)
    print('User: ' + str(callback.message.from_user.id))
        bot.send_message(callback.message.chat.id, gr2(callback))
    if callback.data == 'study-po-1':
        bot.send_message(callback.message.chat.id, gr1(callback))'''


@bot.message_handler(commands=['gr1'])
def gr1(message):
    print('User ' + str(message.from_user.id))
    bot.send_message(message.from_user.id, rw(gr='ПО-1'))


@bot.message_handler(commands=['gr2'])
def gr2(message):
    print('User ' + str(message.from_user.id))
    bot.send_message(message.from_user.id, rw(gr='ЭС-2'))


bot.polling(none_stop=True, timeout=10000)
