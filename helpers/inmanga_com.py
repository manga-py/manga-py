from json import loads
from requests import get
from os import system, path

_path = path.dirname(path.dirname(path.realpath(__file__)))

all_manga_list = None
n = 0
while n < 10:
    try:
        all_manga_list = loads(get('http://inmanga.com/OnMangaQuickSearch/Source/QSMangaList.json').text)
        break
    except Exception:
        pass
    n += 1
if not all_manga_list:
    print('Error! QSMangaList is not correct json?')

for i in all_manga_list:
    print('Downloading %s' % i['Name'])
    _str = 'cd {}; python3 manga.py --cli -i -u http://inmanga.com/ver/manga/{}/{}'
    system(_str.format(_path, i['Name'], i['Name'], i['Identification']))
