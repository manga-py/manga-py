from time import time
from urllib import parse

from manga_py.crypt.puzzle import Puzzle
from manga_py.fs import rename
from manga_py.provider import Provider
from .helpers.std import Std


class PlusComicoJp(Provider, Std):
    scrambles = []

    def get_chapter_index(self) -> str:
        return self.re.search('/store/\d+/(\d+)', self.chapter).group(1)

    def get_content(self):
        content = self._storage.get('main_content', None)
        if content:
            return content
        idx = self.re.search('/store/(\d+)', self.get_url())
        url = '{}/store/{}/'.format(self.domain, idx.group(1))
        return self.http_get(url)

    def get_manga_name(self) -> str:
        return self.text_content(self.content, 'h1 > ._title')

    def get_chapters(self):
        idx = self.re.search(r'/store/(\d+)', self.get_url()).group(1)
        data = self.http_post('{}/store/api/getTitleArticles.nhn'.format(
            self.domain
        ), data={
            'titleNo': idx
        })
        json = self.json.loads(data)
        items = []
        for i in json.get('result', {}).get('list', {}):
            for m in i.get('articleList'):
                if m.get('freeFlg') == 'Y':
                    items.append(m.get('articleDetailUrl'))
        return items

    def get_files(self):
        url = self.http().requests(self.chapter, method='head')
        location = url.headers.get('location')
        self.http().requests(location, method='head')

        location = parse.urlparse(location)
        params = parse.parse_qs(location.query)

        ts = int(time())
        base_url = '{}://{}{}/diazepam_hybrid.php?param={}&ts={}&_={}&reqtype=0'.format(
            location.scheme,
            location.netloc,
            self.re.search(r'(.+)/\w+\.php', location.path).group(1),
            parse.quote_plus(params.get('param')[0]),
            ts,
            ts + 1305,
        )

        pages_url = base_url + '&mode=7&file=face.xml&callback=jQ12_34'
        scramble_url = base_url + '&mode=8&file={:0>4}.xml'
        file_url = base_url + '&mode=1&file={:0>4}_0000.bin'

        total_pages = self.re.search(r'TotalPage>(\d+)</TotalPage', self.http_get(pages_url))
        if total_pages:
            total_pages = int(total_pages.group(1))
        else:
            total_pages = 0
        items = []
        self.scrambles = []
        for i in range(total_pages):
            c = self.re.search(r'Scramble>(.+?)</Scramble', self.http_get(scramble_url.format(i)))
            self.scrambles.append(c.group(1))
            items.append(file_url.format(i))
        return items

    def get_cover(self) -> str:
        return self._cover_from_content('.cover img')

    def after_file_save(self, _path: str, idx: int):
        _matrix = self.scrambles[idx].split(',')
        div_num = 4
        matrix = {}
        n = 0
        for i in _matrix:
            matrix[int(i)] = n
            n += 1
        p = Puzzle(div_num, div_num, matrix, 8)
        p.need_copy_orig = True
        p.de_scramble(_path, '{}.jpg'.format(_path))
        rename('{}.jpg'.format(_path), _path)
        return _path, None

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        if in_arc_name is None:
            in_arc_name = '{}_image.jpg'.format(idx)
        super().save_file(idx, callback, url, in_arc_name)

    def book_meta(self) -> dict:
        # todo meta
        pass


main = PlusComicoJp
