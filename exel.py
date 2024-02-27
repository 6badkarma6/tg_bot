def rw(gr: str):
    data = ajson()
    return message(nn(lists=message_dt(gr=gr, load_file=data['sso'])))


def nn(lists: list) -> list:
    for j in lists:
        for k in j:
            if k == 'None' and j.index(k) != 4:
                print(j)
                lists[lists.index(j)][j.index(k)] = lists[lists.index(j) - 1][j.index(k)]
    return lists


def message(data: list) -> str:
    ms = ''
    for i in data:
        for w in i:
            ms = ms + w
    return ms


def message_dt(gr: str, load_file: str, file: str = 'data.json') -> list:
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
                # and x != data[gr]['x'][3] and y != data[gr]['y'][3]:
                dt.append(str(sh[f'{x}{y}'].value))
                # dt.append('     ')
            elif str(sh[f'{x}{y}'].value) == 'None' and x != data[gr]['x'][0] and y != data[gr]['y'][0]:
                # and x != data[gr]['x'][4] and y != data[gr]['y'][3]:
                dt.append(str(sh[f'{x}{y}'].value))
                # dt.append('     ')
            elif str(sh[f'{x}{y}'].value) == 'None':
                dt.append('     ')
            else:
                dt.append(str(sh[f'{x}{y}'].value) + '    ')
        dt.append('\n')
        message_data.append(dt)
    return message_data


def src():
    import os
    os.system("curl -o page_source.html https://vgke.by/raspisanie-zanjatij/")


def pr():
    from bs4 import BeautifulSoup
    import json
    with open("page_source.html") as html:
        print('pr start')
        soup = BeautifulSoup(html, 'html.parser')
        data = []
        http = []
        name = []
        for link in soup.find_all('iframe'):
            data.append(link.get('src'))
        for i in range(len(data)):
            ds = i
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


def save(pb=False):
    import os
    if pb:
        pr()
        print('pr True')
    print('start...')
    data = ajson()
    # os.system('cd /mnt/d/Tg/download')
    os.system("curl -O " + data['http_sso'])
    print('...finish')


def ajson(file: str = 'conf.json'):
    import json
    with open(file, 'r') as file:
        date = json.load(file)
    return date


def sort(file: str):
    import openpyxl
    file = openpyxl.load_workbook(file)
    open_file = file.active
    sn = {}
    i = 2
    while True:
        r = 5
        r += i
        if open_file.cell(row=r, column=3).value == ' ':
            i += 1
            sn['y'] = i
            break
        i += 2
    o = 1
    while True:
        ln = 3
        ln += o
        if open_file.cell(row=4, column=ln).value != 'None':
            o += 1
            sn['x'] = o
            break
        o += 1
    for i in range(1, open_file.max_row):
        for j in range(1, open_file.max_column):
            if open_file.cell(row=i, column=j).value == 'ПО-1':
                sn['po-r'] = [4, i]
                sn['po-a'] = [3, j]
            if open_file.cell(row=i, column=j).value == 'ЭС-2':
                sn['es-r'] = [4, i]
                sn['es-a'] = [3, j]
    return sn


def ls(a: int, r: int, x: int = 3, y: int = 7) -> tuple[list[str], list[str]]:
    abc = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']
    row = []
    column = []
    for i in range(0, x):
        k = abc[a]
        column.append(f'{k}')
        a += 1
    for j in range(0, y):
        row.append(f'{r}')
        r += 1
    return column, row


def data_conf():
    with open('data.json', 'w') as file:
        import json
        data = ajson()
        sn = sort(data['sso'])
        po_x, trash = ls(sn['po-a'][0], sn['po-r'][0], y=sn['y'], x=sn['x'])
        po_z, po_y = ls(sn['po-a'][1], sn['po-r'][1], y=sn['y'])
        po_x = po_x + po_z
        es_x, trash = ls(sn['es-a'][0], sn['es-r'][0], y=sn['y'], x=sn['x'])
        es_z, es_y = ls(sn['es-a'][1], sn['es-r'][1], y=sn['y'])
        es_x = es_x + es_z
        json.dump({'ПО-1': {'x': po_x, 'y': po_y},
                   'ЭС-2': {'x': es_x, 'y': es_y}}, file)

# if __name__ == "__main__":
#    pr()
#    save()
