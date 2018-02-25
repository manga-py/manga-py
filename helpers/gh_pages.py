from src.providers import providers_list

start_items = [
    ['http://bato.to', 0, ' - Batoto will be closing down permanently (Jan 18, 2018)'],
    ['http://bulumanga.com', 0, ' - Closed'],
    ['http://bwahahacomics.ru', 0, ' - Very little content. Possibly, will be done in the future.'],
    ['http://com-x.life', 1, ' - One thread only!!! --no-multi-threads. <i class="v0"></i>'],
    ['http://comic-walker.com', 0, ' - Maybe...'],
    ['http://comico.jp', 1, ' - only public downloading now'],
    ['http://comixology.com', 0, ' - Buy only. Not reading.'],
    ['http://e-hentai.org', 1, '<i class="td"></i>'],
    ['http://eatmanga.me', 1, '<i class="v0"></i>'],
    ['http://gogomanga.co', 1, '<i class="v0"></i>'],
    ['http://hentai-chan.me', 1, '- Need fill access file'],
    ['http://heymanga.me', 1, '<i class="v0"></i>'],
    ['http://comic.k-manga.jp', 0, ' - Maybe...'],
    ['http://luscious.net', 1, '<i class="td"></i>'],
    ['http://lezhin.com', 0, ' - Maybe...'],
    ['http://mangaforall.com', 1, ''],
    ['http://mangafreak.net', 1, '<i class="v0"></i>, site down now'],
    ['http://mangahead.me', 1, '<i class="v0"></i>, site down now'],
    ['http://mangaleader.com', 1, '<i class="v0"></i> site down now'],
    ['http://mangamove.com', 1, '<i class="v0"></i>, site down now'],
    ['http://manganel.com', 1, '<i class="v0"></i>, site down now'],
    ['http://mangaroot.com', 1, '<i class="v0"></i>, site down now, one thread only!!! --no-multi-threads'],
    ['http://mangaz.com', 0, ' - Maybe...'],
    ['http://mg-zip.com', 0, ' - Will not be implemented'],
    ['http://rawdevart.com', 1, '<i class="v0"></i>, very little content'],
    ['http://s-manga.net', 0, ' - Maybe'],
    ['http://tapas.io', 1, '<i class="v0"></i>, only public downloading now'],
    ['http://zip.raw.im', 0, ' - Will not be implemented'],
]

_list = [providers_list[n] for n in providers_list.keys()]
items = []
for i in _list:
    items += i
_items = [n.replace(r'\.', '.') for n in items]
_list = {}
for i in _items:
    _ = i[:i.find('/')].strip('()')
    _list[_] = _
_unique = [i[0] for i in start_items]
items = []
for i in _list:
    if i not in _unique:
        items.append([i, 1, ''])
items += start_items
items = sorted(items, key=lambda l: l[0])
print(items)  # Ohh...
