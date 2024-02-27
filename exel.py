
def rw():
    data = ajson()
    return message(nn(lists=message_dt(load_file=data['sso'])))


def nn(lists: list) -> list:
    for j in lists:
        for k in j:
            if k == 'None':
                lists[lists.index(j)][j.index(k)] = lists[lists.index(j)-1][j.index(k)]
    return lists


def message(data: list) -> str:
    ms = ''
    for i in data:
        for w in i:
            ms = ms + w
    return ms


def message_dt(load_file: str, file: str = 'data.json') -> list:
    import openpyxl
    wb = openpyxl.load_workbook(load_file)
    sh = wb.active
    data = ajson(file)
    message_data = []
    xd = data['x']
    yd = data['y']
    for y in yd:
        dt = []
        for x in xd:
            if str(sh[f'{x}{y}'].value) == 'None' and x != data['x'][0] and y != data['y'][0] and x != data['x'][3]:
                # dt.append(str(sh[f'{x}{y}'].value))
                dt.append('     ')
            elif str(sh[f'{x}{y}'].value) == 'None' and x != data['x'][0] and y != data['y'][0] and x != data['x'][4]:
                # dt.append(str(sh[f'{x}{y}'].value))
                dt.append('     ')
            elif str(sh[f'{x}{y}'].value) == 'None':
                dt.append('     ')
            else:
                dt.append(str(sh[f'{x}{y}'].value) + '    ')
        dt.append('\n')
        message_data.append(dt)
    return message_data


def src():
    import os
    os.system("curl -o page_source.html " + "https://vgke.by/raspisanie-zanjatij/")


def pr():
    from bs4 import BeautifulSoup
    import json
    print('src start')
    src()
    print('src finish')
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
                sso = data[ds][-12:]
                http_sso = data[ds][51:]
            if name[ds][:7] == 'den-sso' and name[ds][7] == '-':
                sso = data[ds][-14:]
                http_sso = data[ds][51:]
        print('pr finish')
        with open('conf.json', 'w') as write_file:
            json.dump({'http': http, 'http-sso': http_sso, 'name': name, 'sso': sso}, write_file)
        return True


def save(pb=False):
    import os
    if pb:
        pr()
        print('pr True')
    print('start...')
    data = ajson()
    # os.system('cd /mnt/d/Tg/download')
    os.system("curl -O " + data['http-sso'])
    print('...finish')


def ajson(file: str = 'conf.json'):
    import json
    with open(file, 'r') as file:
        date = json.load(file)
    return date
