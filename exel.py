"""Модули для бота"""


def lon(data) -> str:
    string = ' Список групп: '
    for i in range(len(data)):
        string = string + data[i] + ' '
    return string


def rw(group: str) -> str:
    """Вывод строки с рассписанием группы"""
    # data = ajson()
    # return message(nn(lists=message_dt(gr=gr, load_file=data['sso'])))
    groups = ajson("timetable.json")
    return groups[group]


def time_grs():
    import json
    time = {}
    data = ajson()
    list_grs = ajson('bin.json')
    list_grs = list_grs['grs']
    for i in list_grs:
        print(type(i), i)
        time[i] = message(nn(lists=message_dt(gr=i, load_file=data['sso'])))
    print(time)
    with open('timetable.json', 'w') as file:
        json.dump(time, file, indent=2)
    return True


# Фильтр
def nn(lists: list) -> list:
    """Фильтрует от пустых строк и добавляет недостоющие"""
    for j in range(len(lists)):
        for k in range(len(lists[j])):
            if lists[j][k] == 'None' and j != 3:
                lists[j][k] = lists[j - 1][k]
    for j in range(len(lists)):
        for k in range(len(lists[j])):
            if lists[j][k] == 'None':
                lists[j][k] = '     '
    return lists


# Форматирует список в текст
def message(data: list) -> str:
    """Преобразует список в текст"""
    return ''.join([''.join(dt) for dt in data])


# Формирует список
def message_dt(gr: str, load_file: str, file: str = 'data.json') -> list:
    """Формирует список из .xlsx файла по конфигурации data.json"""
    import openpyxl
    wb = openpyxl.load_workbook(load_file)
    sh = wb.active
    data = ajson(file)
    message_data = []
    xd = data[gr]['x']
    yd = data[gr]['y']
    for y in yd:
        dt = []
        for x in xd:
            if str(sh[f'{x}{y}'].value) == 'None' and x != data[gr]['x'][0] and y != data[gr]['y'][0]:
                dt.append(str(sh[f'{x}{y}'].value))
            elif str(sh[f'{x}{y}'].value) == 'None':
                dt.append('     ')
            else:
                dt.append(str(sh[f'{x}{y}'].value) + '    ')
        dt.append('\n')
        message_data.append(dt)
    return message_data


# Сохраняет HTML формат страницы
def src():
    """Сохраняет исходный код страницы"""
    import os
    os.system("curl -o page_source.html https://vgke.by/raspisanie-zanjatij/")
    return True


# Достаёт из исходного кода нужные ссылки и названия
def pr():
    """Достаёт из исходного кода нужные ссылки и названия"""
    from bs4 import BeautifulSoup
    import json
    with open(file='page_source.html', mode='r', encoding='utf-8') as html:
        print('pr start')
        soup = BeautifulSoup(html, 'html.parser')
        data = []
        http = []
        name = []
        for link in soup.find_all('iframe'):
            data.append(link.get('src'))
        for j in range(len(data)):
            ds = j
            http.append(data[ds][51:])
            if data[ds][-17] == '/':
                name.append(data[ds][-16:])
            elif data[ds][-13] == '/':
                name.append(data[ds][-12:])
            elif data[ds][-15] == '/':
                name.append(data[ds][-14:])
            else:
                name.append(data[ds][-15:])
            if name[ds][:7] == 'den-sso':
                sso = str(data[ds][-12:])
                http_sso = str(data[ds][51:])
            if name[ds][:7] == 'den-sso' and name[ds][7] == '-':
                sso = str(data[ds][-14:])
                http_sso = str(data[ds][51:])
        print('pr finish')
        with open('conf.json', 'w') as write_file:
            json.dump({'http': http,
                       'http_sso': http_sso,
                       'name': name,
                       'sso': sso}, write_file, indent=2)
        return True


# Сохраняет файл
def save(pb=False):
    """Сохраняет файл"""
    import os
    if pb:
        pr()
        print('pr True')
    print('start...')
    data = ajson()
    os.system("curl -O " + data['http_sso'])
    print('...finish')


# Импортирует данные файла conf.json
def ajson(file: str = 'conf.json'):
    """Импортирует данные"""
    import json
    with open(file, 'r') as file:
        data = json.load(file)
    return data


# Сортирует exel файл
def search(file: str, gr: str):
    """Сортирует exel файл"""
    import openpyxl
    workbook = openpyxl.load_workbook(file)
    open_file = workbook.active
    for gr_x in range(1, open_file.max_row):
        for gr_y in range(1, open_file.max_column):
            if open_file.cell(row=gr_x, column=gr_y).value == gr:
                return gr_x, gr_y


def filters(file: str, gr_x: int, gr_y: int, gr: str):
    # data = ajson('bin.json')
    import openpyxl
    workbook = openpyxl.load_workbook(file)
    open_file = workbook.active
    x = gr_x
    # print(x, end=' ')
    y = 3
    # print(y)
    for i in range(14):
        x += 1
        if str(open_file.cell(row=x, column=y).value) == '' or str(open_file.cell(row=x, column=y).value) == ' ':
            # print('break', x, open_file.cell(row=x, column=y).value)
            x -= 1
            if gr == 'ЭС-2':
                x -= 1
            break
        # print(x, open_file.cell(row=x, column=y).value)
    for i in range(4):
        if str(open_file.cell(row=gr_x, column=y).value) == 'None':
            # print('break')
            break
        y += 1
        # print(y, open_file.cell(row=x, column=gr_y).value)
    if str(open_file.cell(row=gr_x, column=g(1, gr_y)).value) == 'None' \
            and str(open_file.cell(row=gr_x, column=g(3, gr_y)).value) == 'None':
        gr_y += 3
    elif str(open_file.cell(row=gr_x, column=g(1, gr_y)).value) == 'None' \
            and str(open_file.cell(row=gr_x, column=g(3, gr_y)).value) != 'None' or \
            str(open_file.cell(row=gr_x, column=g(1, gr_y)).value) != 'None' \
            and str(open_file.cell(row=gr_x, column=g(2, gr_y)).value) == 'None':
        gr_y += 2
    else:
        gr_y += 1
    return x, y, gr_y


def g(x: int, y: int):
    return x + y


# Состовляет столбцы и строки
def ls(gr_x: int, gr_y1: int, gr_y2, x: int, y: int, y0: int = 3, k: int = 1) -> tuple[list[str], list[str]]:
    # [gr_x, 3, x, y], [gr_x, gr_y1, x, gr_y2]
    import json
    with open('bin.json', 'r') as file:
        data = json.load(file)
    abc = data['abc']
    row = []
    column = []
    r_glob = x - gr_x + k
    c_timing = y - y0 + k
    c_gr = gr_y2 - gr_y1 + k
    for n in range(0, r_glob):
        row.append(str(g(gr_x, n)))
    for i in range(0, c_timing):
        column.append(abc[g(y0, i)])
    for j in range(0, c_gr):
        column.append(abc[g(gr_y1, j)])
    return column, row


# Формирует конфигурационный файл data.json
def data_conf():
    import json
    conf = ajson()
    binarn = ajson('bin.json')
    grs = binarn['grs']
    file = conf['sso']
    with open(file='data.json', mode='w', encoding='utf-8') as dump_file:
        dump = {}
        for gr in grs:
            print("start ", gr)
            gr_x, gr_y1 = search(file, gr)
            x, y, gr_y2 = filters(file, gr_x, gr_y1, gr)
            column, row = ls(gr_x=gr_x, gr_y1=gr_y1, x=x, y=y, gr_y2=gr_y2)
            dt = dict(x=column, y=row)
            print(dt, end='\n\n')
            dump[gr] = dt
        print(dump)
        json.dump(obj=dump, fp=dump_file, indent=4)
    return time_grs()


# Считывет токин бота
def data() -> str:
    # with open('bot', 'r') as data_bot:
    with open('badwr', 'r') as data_bot:
        return data_bot.read(46)


def info(message, name):
    import datetime
    print(datetime.datetime.fromtimestamp(message.date), end=': ')
    print(name.from_user.first_name, end=' ')
    print(name.from_user.id)


class Users:
    def __init__(self):
        self.db = None

    def read_user(self):
        db = {}
        import shelve as sh
        with sh.open("user\\user_id", flag='r') as file:
            for i in file:
                db[i] = file[i]
        self.db = db

    def check_id(self, user_id: str) -> bool:
        if user_id in self.db:
            return True
        else:
            return False

    @staticmethod
    def add_user(user_id: str, first_name: str, group: str):
        import shelve as sh
        with sh.open("user\\user_id", flag='c') as file:
            file[user_id] = [first_name, group]

    @staticmethod
    def del_user(user_id: str):
        import shelve as sh
        with sh.open("user\\user_id", flag='c') as file:
            del file[user_id]

    def post_user(self):
        return self.db

# if __name__ == "__main__":
# import json
# file = "den-sso-1.xlsx"
# gr = str(input('>>'))
# gr_x, gr_y1 = search(file, gr)
# x, y, gr_y2 = filter(file, gr_x, gr_y1, gr)
# print([gr_x, 3, x, y], [gr_x, gr_y1, x, gr_y2])
# column, row = ls(gr_x=gr_x, gr_y1=gr_y1, x=x, y=y, gr_y2=gr_y2)
# print(column, row)
# data_conf()
# print(rw('ПО-1'))
# print(user(1234))
# inp = int(input('>>'))
# print(user(inp))
