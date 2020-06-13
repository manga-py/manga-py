from manga_py.providers import providers_list
from manga_py.fs import root_path
from manga_py.meta import repo_name
from json import dumps
from datetime import datetime

start_items = [
    # [ address, (0 - not worked, 1 - worked, 2 - alias), 'Comment']
    ['http://com-x.life', 1, ' - One thread only!!! --no-multi-threads. <i class="v0"></i>'],
    ['http://comic-walker.com', 0, ' - Maybe...'],
    ['http://comico.jp', 1, ' - only public downloading now'],
    ['http://e-hentai.org', 1, '<i class="td"></i>'],
    ['http://dm5.com', 0, '<i class="d"></i> <b>Site down now</b>'],
    ['http://heavenmanga.biz', 2, '- See heavenmanga.site'],
    ['http://hentai-chan.me', 1, '- Need fill access file'],
    ['http://comic.k-manga.jp', 0, ' - Maybe...'],
    ['http://luscious.net', 1, '<i class="td"></i>'],
    ['http://lezhin.com', 0, ' - Maybe...'],
    ['http://mangaz.com', 0, ' - Maybe...'],
    ['http://s-manga.net', 0, ' - Maybe'],
    ['http://sunday-webry.com', 0, ' - Not worked decryption images now. In develop.'],
    ['http://tapas.io', 1, '<i class="v0"></i>, only public downloading now'],
    ['http://tsumino.com', 1, '<i class="d"></i>'],
    ['http://8muses.com', 0, '- Need decode page.'],
    ['http://mangago.me', 0, '- Need decode page.'],

    ['http://mangachan.me', 1, '- Site down now.'],

    ['http://digitalteamreader.netsons.org', 0, ' - Moved to http://dgtread.com Maybe later'],
    ['http://hentai-chan.me', 0, ' - Malicious site. Not recommended for visiting'],
    ['http://kobato.hologfx.com/reader', 1, ' - Reader offline'],
    ['http://mangaid.co', 1, ' - See https://bacamanga.co/'],
    ['http://reader.championscans.comco', 0, ' - See read.ptscans.com'],
    ['http://http://reader.jokerfansub.com', 0, ' - Site down now'],
]


_start_items = [i[0] for i in start_items]


def merge(*providers):
    for p in providers:
        yield from providers_list[p]


def clean(providers):
    _list = {}
    for i in providers:
        _ = i.find('/')
        if not ~_:
            _ = i.strip('()')
        else:
            _ = i[:_].strip('()')
        _list['http://' + _.replace(r'\.', '.')] = ''
    return list(_list.keys())


def aggregate(providers):
    _list = []
    for i in providers:
        if i not in _start_items:
            _list.append([i, 1, ''])
    return _list


def prepare_html(html):
    with open(html, 'r') as r:
        content = r.read()
    with open(html, 'w') as w:
        content = content.replace('__repo_name__', repo_name)
        today = datetime.today()
        content = content.replace('__last_update__', '{}/{:0>2}/{:0>2} {:0>2}-{:0>2}-{:0>2}'.format(
            today.year, today.month, today.day, today.hour, today.minute, today.second
        ))
        w.write(content)


def build_providers():
    items = aggregate(clean(merge(*providers_list))) + start_items
    items = sorted(items, key=lambda l: l[0])
    return dumps(items)


def main():
    path = root_path() + '/helpers/gh_pages_content/'
    with open(path + 'providers.json', 'w') as w:
        w.write(build_providers())
    prepare_html(path + 'index.html')
    prepare_html(path + 'improvement.html')


# print(len(build_providers()))

