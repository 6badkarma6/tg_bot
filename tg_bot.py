# Проверка на наличие библиотек
try:
    import telebot
    from telebot import types
    from exel import rw, data
except Exception as error:
    raise error
finally:
    print("Функции успешно импортированны")

# Взятие токена и его инициализация
bot = telebot.TeleBot(data())


@bot.message_handler(commands=['start'])
def start(message):
    """Функция настройки бота при его старте"""
    print('User ' + str(message.from_user.id))
    c1 = types.BotCommand(command='start', description='Start the Bot')
    c2 = types.BotCommand(command='gr1', description='Расписание ПО-1')
    c3 = types.BotCommand(command='gr2', description='Расписание ЭС-2')
    bot.set_my_commands([c1, c2, c3])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Расписание ПО-1", callback_data='study-po-1'))
    markup.add(types.InlineKeyboardButton("Расписание ЭС-2", callback_data='study-es-2'))
    bot.send_message(message.from_user.id, ' Bot v0.3b \n Работает с 15:00 по 21:00', reply_markup=markup)


# Отвечает на callback.data
@bot.callback_query_handler(func=lambda callback: True)
def study(callback):
    """Отвечает на InLineKeyboardButton"""
    if callback.data == 'study-po-1':
        print('User in callback po-1: ' + str(callback.from_user.id))
        bot.send_message(callback.from_user.id, rw(gr='ПО-1'),
                         protect_content=True,
                         disable_notification=True)
    if callback.data == 'study-es-2':
        print('User in callback es-2: ' + str(callback.from_user.id))
        bot.send_message(callback.from_user.id, rw(gr='ЭС-2'),
                         protect_content=True,
                         disable_notification=True)


# Выводит рассписание группы номер 1
@bot.message_handler(commands=['gr1'])
def gr1(message):
    """Рассписание группы номер 1"""
    print('User in gr1: ' + str(message.from_user.id))
    bot.send_message(message.from_user.id, rw(gr='ПО-1'),
                     protect_content=True,
                     disable_notification=True)


# Выводит рассписание группы номер 2
@bot.message_handler(commands=['gr2'])
def gr2(message):
    """Рассписание группы номер 2"""
    print('User in gr2: ' + str(message.from_user.id))
    bot.send_message(message.from_user.id, rw(gr='ЭС-2'),
                     protect_content=True,
                     disable_notification=True)


@bot.message_handler(commands=['adm'])
def adm(message):
    """Админ панель для тестов"""
    if message.chat.id == 1474943294:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Расписание ПО-1", callback_data='study-po-1'))
        bot.send_message(message.from_user.id, message,
                         reply_markup=markup,
                         protect_content=True,
                         disable_notification=True)


print('bot start')
try:
    bot.polling(none_stop=True,
                timeout=10000)
finally:
    print('bot finish')
