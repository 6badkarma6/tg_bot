import telebot
from telebot import types

from exel import rw

bot = telebot.TeleBot('6788562469:AAFvF-l8F9cJrUJeYSyCsLdnPR7TbyyqbS8')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Расписание", callback_data='study'))
    bot.send_message(message.from_user.id, ' Bot v0.1a', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def study(callback):
    if callback.data == 'study':
        bot.send_message(callback.message.chat.id, rw(), parse_mode='html')


@bot.message_handler(commands=['stop'])
def stop():
    raise SystemError('Program stopped')


bot.polling(none_stop=True)
