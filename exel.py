"""Модули для бота"""


def rw(gr: str):
    """Вывод строки с рассписанием группы"""
    data = ajson()
    return message(nn(lists=message_dt(gr=gr, load_file=data['sso'])))


# Фильтр
def nn(lists: list) -> list:
    """Фильтрует от пустых строк и добавляет недостоющие"""
    for j in range(len(lists)):
        for k in range(len(lists[j])):
            if lists[j][k] == 'None' and j != 3:
                lists[j][k] = lists[j-1][k]
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
            elif str(sh[f'{x}{y}'].value) == 'None' and x != data[gr]['x'][0] and y != data[gr]['y'][0]:
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
            json.dump({'http': http, 'http_sso': http_sso, 'name': name, 'sso': sso}, write_file)
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
        date = json.load(file)
    return date


# Сортирует exel файл
def sort(file: str):
    """Сортирует exel файл"""
    import openpyxl
    file = openpyxl.load_workbook(file)
    open_file = file.active
    sn = {}
    j = 0
    while range(100000):
        r = 4
        r += j
        if open_file.cell(row=r, column=3).value == '' or open_file.cell(row=r, column=3).value == ' ':
            sn['y'] = j
            break
        j += 1
    o = 1
    while range(10000):
        ln = 3
        ln += o
        if open_file.cell(row=4, column=ln).value != 'None':
            o += 1
            sn['x'] = o
            break
        o += 1
    for j in range(1, open_file.max_row):
        for k in range(1, open_file.max_column):
            if open_file.cell(row=j, column=k).value == 'ПО-1':
                sn['po-r'] = [4, j]
                sn['po-c'] = [3, k]
            if open_file.cell(row=j, column=k).value == 'ЭС-2':
                sn['es-r'] = [4, j]
                sn['es-c'] = [3, k]
    return sn


# Состовляет столбцы и строки
def ls(a: int, r: int, x: int = 3, y: int = 7) -> tuple[list[str], list[str]]:
    abc = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']
    row = []
    column = []
    for n in range(0, x):
        k = abc[a]
        column.append(f'{k}')
        a += 1
    for j in range(0, y):
        row.append(f'{r}')
        r += 1
    return column, row


# Формирует конфигурационный файл data.json
def data_conf():
    with open('data.json', 'w', encoding='utf-8') as file:
        import json
        data = ajson()
        sn = sort(data['sso'])
        po_x, trash = ls(sn['po-c'][0], sn['po-r'][0], y=sn['y'], x=sn['x'])
        po_z, po_y = ls(sn['po-c'][1], sn['po-r'][1], y=sn['y'])
        po_x = po_x + po_z
        es_x, trash = ls(sn['es-c'][0], sn['es-r'][0], y=sn['y'], x=sn['x'])
        es_z, es_y = ls(sn['es-c'][1], sn['es-r'][1], y=sn['y'])
        es_x = es_x + es_z
        json.dump({'ПО-1': {'x': po_x, 'y': po_y},
                   'ЭС-2': {'x': es_x, 'y': es_y}}, file)


# Считывет токин бота
def data() -> str:
    with open('bot', 'r') as data_bot:
        return data_bot.read()
