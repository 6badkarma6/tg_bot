"""БОТ в Телеграмм"""

# Проверка на наличие библиотек
try:
    import telebot
    from telebot import types
    from exel import rw, data, info, ajson, lon, Users
except Exception as error:
    raise error
finally:
    print("Функции успешно импортированны")

# Взятие токена и его инициализация
bot = telebot.TeleBot(data())


@bot.message_handler(commands=['start'])
def start(message):
    """Функция настройки бота при его старте"""
    print('User ', end=' ')
    info(message, message)
    c1 = types.BotCommand(command='start', description='Start the Bot')
    c2 = types.BotCommand(command='gr', description='Print time for group')
    c3 = types.BotCommand(command='list', description='Return list of group')
    c4 = types.BotCommand(command='help', description='Return help doc')
    bot.set_my_commands([c1, c2, c3, c4])
    try:
        bot.send_message(message.from_user.id, ' Bot v1 \n  работает',
                         protect_content=True,
                         disable_notification=True)
    except BaseException:
        print('exept')


# Отвечает на callback.data
@bot.callback_query_handler(func=lambda callback: True)
def study(callback):
    """Отвечает на InLineKeyboardButton"""
    if callback.data == 'study-po-1':
        print('User in callback po-1: ', end='')
        info(callback.message, callback)
        try:
            bot.send_message(callback.from_user.id, rw(group='ПО-1'),
                             protect_content=True,
                             disable_notification=True)
        except BaseException:
            print('exept')
    if callback.data == 'study-es-2':
        print('User in callback es-2: ', end='')
        info(callback.message, callback)
        try:
            bot.send_message(callback.from_user.id, rw(group='ЭС-2'),
                             protect_content=True,
                             disable_notification=True)
        except BaseException:
            print('exept')


# Выводит рассписание группы номер 1
@bot.message_handler(commands=['list'])
def list(message):
    """Рассписание группы номер 1"""
    print('User in list: ', end='')
    info(message, message)
    data = ajson('bin.json')
    try:
        bot.send_message(message.from_user.id, lon(data['grs']),
                         protect_content=True,
                         disable_notification=True)
    except BaseException:
        print('exept')



@bot.message_handler(commands=['help'])
def help(message):
    """Рассписание группы номер 2"""
    print('User in help: ', end='')
    info(message, message)
    doc = """
    * для начало работы и сброса пред настрое бота ввежите '/start'
    * для вывода списка доступных групп введите '/list'
    * для вывода раписания для доступных группы введите '/gr -*-'
    -*- — группа из списка групп
"""
    try:
         bot.send_message(message.from_user.id, doc,
                          protect_content=True,
                          disable_notification=True)
    except BaseException:
         print('exept')


@bot.message_handler(commands=['gr'])
def gr(message):
    """Рассписание групп"""
    print('User in gr: ', end='')
    info(message, message)
    text = message.text.split(' ')
    if len(text) == 1:
       bot.send_message(message.from_user.id, 'Не правильно введена команда',
                         protect_content=True,
                         disable_notification=True)
    try:
        group = text[1].upper()
        print(group)
        bot.send_message(message.from_user.id, rw(group=group),
                         protect_content=True,
                         disable_notification=True)
    except BaseException:
        print('exept')


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
    bot.polling(none_stop=True, timeout=10000)
finally:
    print('bot finish')
