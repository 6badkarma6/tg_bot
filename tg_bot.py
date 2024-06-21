"""БОТ в Телеграмм"""

# Проверка на наличие библиотек
try:
    import telebot
    import logging
    import logging.config
    from telebot import types
    from exel import Modules as Modules, Users
    import datetime
except Exception as error:
    raise error
finally:
    print("Функции успешно импортированны")

logger = logging.getLogger('')
logging.basicConfig(filename='log.txt',
                    encoding="utf-8",
                    level=logging.INFO,
                    format='%(asctime)s  %(message)s ',
                    datefmt='%m/%d/%Y %H:%M:%S')

# Взятие токена и его инициализация
bot = telebot.TeleBot(Modules.data())
user = Users()
user.read_user()
ids = user.post_user()


@bot.message_handler(commands=['start'])
def start(message):
    """Функция настройки бота при его старте"""
    logger.info('User with id {0} press start in {1}[#]'.format(message.from_user.id,
                                                                Modules.info(message, message)))
    c1 = types.BotCommand(command='start', description='Start the Bot')
    c2 = types.BotCommand(command='gr', description='Print time for group')
    c3 = types.BotCommand(command='list', description='Return list of group')
    c4 = types.BotCommand(command='help', description='Return help doc')
    c5 = types.BotCommand(command='add_user', description='auto notification')
    bot.set_my_commands([c1, c2, c3, c4, c5])
    try:
        bot.send_message(message.from_user.id, ' Bot v1 \n  работает с 16:40 по 21:00 ',
                         protect_content=True,
                         disable_notification=True)
    except ConnectionError:
        print('except')
    else:
        print("Just start error")


# Выводит рассписание группы номер 1
@bot.message_handler(commands=['list'])
def lists(message):
    """Рассписание группы номер 1"""
    logger.info('[#]User with id {0} press list in {1}[#]'.format(message.from_user.id,
                                                                  Modules.info(message, message)))
    data = Modules.ajson(file="bin.json")
    try:
        bot.send_message(message.from_user.id, Modules.lon(data['grs']),
                         protect_content=True,
                         disable_notification=True)
    except ConnectionError:
        print('[!] except')
    else:
        print("Just list error")


@bot.message_handler(commands=['help'])
def helps(message):
    """Рассписание группы номер 2"""
    logger.info('[#]User with id {0} press help in {1}[#]'.format(message.from_user.id,
                                                                  Modules.info(message, message)))
    doc = """
    * для начала работы и сброса преднастроек бота введите '/start'
    * для вывода списка доступных групп введите '/list'
    * для вывода раписания для доступных группы введите '/gr -*-'
    -*- — группа из списка групп
    *
    *для включения авто уведомления введите '/add_user -*-'
"""
    try:
        bot.send_message(message.from_user.id, doc,
                         protect_content=True,
                         disable_notification=True)
    except ConnectionError:
        print('[!] except')
    else:
        print("Just help error")


@bot.message_handler(commands=['gr'])
def gr(message):
    """Рассписание групп"""
    logger.info('[#]User with id {0} press gr in {1}[#]'.format(message.from_user.id,
                                                                Modules.info(message, message)))
    text = message.text.split(' ')
    if len(text) == 1:
        bot.send_message(message.from_user.id, 'Не правильно введена команда',
                         protect_content=True,
                         disable_notification=True)
    try:
        group = text[1].upper()
        print(group)
        bot.send_message(message.from_user.id, Modules.rw(group=group),
                         protect_content=True,
                         disable_notification=True)
    except ConnectionError:
        print('[!] except')
    else:
        print("Just gr error")


@bot.message_handler(commands=['adm'])
def adm(message):
    """Админ панель для тестов"""
    if message.chat.id == 1474943294:
        # markup = types.InlineKeyboardMarkup()
        # markup.add(types.InlineKeyboardButton("Расписание ПО-1", callback_data='study-po-1'))
        bot.send_message(message.from_user.id, message,
                         # reply_markup=markup,
                         protect_content=True,
                         disable_notification=True)


@bot.message_handler(commands=['post'])
def post(message):
    """ post"""
    logger.info('[@] POST [@]')
    if message.chat.id == 1474943294:
        print('post')
        for user_id in ids:
            name, group = ids[user_id]
            bot.send_message(int(user_id), Modules.rw(group), protect_content=False,
                             disable_notification=False)


@bot.message_handler(commands=['add_user'])
def add_user(message):
    """ add"""
    logger.info('[#]User with id {0} press add_user in {1}[#]'.format(message.from_user.id,
                                                                      Modules.info(message, message)))
    global ids
    if str(message.chat.id) in ids:
        bot.send_message(message.chat.id,
                         'user уже зарегестрирован',
                         protect_content=True,
                         disable_notification=True)
    else:
        group = message.text.split(' ')
        try:
            user.add_user(user_id=str(message.chat.id), first_name=message.from_user.first_name, group=group[1].upper())
            bot.send_message(message.chat.id,
                             f"Добавлен пользователь {message.from_user.first_name} с id {message.from_user.id}",
                             protect_content=True,
                             disable_notification=True)
            user.read_user()
            ids = user.post_user()
        except ConnectionError:
            print('[!] except')
            bot.send_message(message.chat.id,
                             'Команда введена неправильно',
                             protect_content=True,
                             disable_notification=True)
        else:
            print("Just notification error")


@bot.message_handler(commands=['del_user'])
def del_user(message):
    """ del"""
    if message.chat.id == 1474943294:
        print('del_user')
        user_id = message.text.split(' ')
        try:
            user.del_user(user_id=user_id[1])
            bot.send_message(message.chat.id,
                             f"пользователь с id {user_id} удалён",
                             protect_content=True,
                             disable_notification=True)
            user.read_user()
            # ids = user.post_user()
        except ConnectionError:
            print('[!] except')
        else:
            print("Just del user error")


@bot.message_handler(commands=['show_user'])
def show_user(message):
    """ show"""
    logger.info('[@] LIST USERS [@]')
    if message.chat.id == 1474943294:
        print('show_users : ', ids)
        try:
            bot.send_message(message.chat.id,
                             f"show_user : {ids}",
                             protect_content=True,
                             disable_notification=True)
        except ConnectionError:
            print('[!] except')
        else:
            print("Just show user error")


@bot.message_handler(commands=['adm_add'])
def adm_add(message):
    """ adm add"""
    if message.chat.id == 1474943294:
        print('adm_add')
        ids = message.text.split(' ')
        if len(ids) == 1:
            try:
                bot.send_message(message.chat.id,
                                 '[!] except',
                                 protect_content=True,
                                 disable_notification=True)
            except ConnectionError:
                print('[!] except')

            else:
                print("Just adm_add.except error")
        try:
            id = ids[1].split(',')
            user.add_user(user_id=id[0], first_name=id[1], group=id[2])
            user.read_user()
            bot.send_message(message.chat.id,
                             str(user.post_user()),
                             protect_content=True,
                             disable_notification=True)
            user.read_user()
            # ids = user.post_user()
        except ConnectionError:
            print('[!] except')
        else:
            print("Just add_users error")


@bot.message_handler(commands=['adm_mes'])
def adm_mes(message):
    """ adm add"""
    if message.chat.id == 1474943294:
        print('adm_mes')
        data = message.text.split(' ')
        if len(data) == 1:
            try:
                bot.send_message(message.chat.id,
                                 '[!] except',
                                 protect_content=True,
                                 disable_notification=True)
            except ConnectionError:
                print('[!] except')
            else:
                print("Just add_mes.except error")
        try:
            id = int(data[1].split('#')[0])
            print(id)
            mes = " ".join((data[1].split('#')[1]).split('-'))
            print(mes)
            bot.send_message(id,
                             mes,
                             protect_content=True,
                             disable_notification=True)
            bot.send_message(message.chat.id,
                             "succes",
                             protect_content=True,
                             disable_notification=True)
        except ConnectionError:
            print('[!] except')
        else:
            print("Just add_mes error")


if __name__ == "__main__":
    try:
        logger.info('[*]bot start[*]')
        print('Бот включен')
        bot.polling(none_stop=True, timeout=10000)
    except ConnectionError as er:
        print('Connection error')
    finally:
        print('Бот выключен')
        logger.info('[*]bot stop[*]')
