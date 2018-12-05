from manga_py.provider import Provider
from .helpers.std import Std
from manga_py.crypt.base_lib import BaseLib


class MangaFoxMe(Provider, Std):

    def get_archive_name(self) -> str:
        groups = self._ch_parser()
        ch = groups[1].replace('.', '-')
        vol = ['0']
        if groups[0]:
            vol = [groups[0]]
        return self.normal_arc_name({'vol': vol, 'ch': ch})

    def _ch_parser(self):
        selector = r'/manga/[^/]+/(?:v([^/]+)/)?c([^/]+)/'
        groups = self.re.search(selector, self.chapter).groups()
        return groups

    def get_chapter_index(self) -> str:
        groups = self._ch_parser()
        idx = groups[1].replace('.', '-')
        if not ~idx.find('-'):
            idx = idx + '-0'
        if groups[0]:
            return '{}-{}'.format(idx, groups[0])
        return idx

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)/?')

    def get_chapters(self):
        return self._elements('#list-1 a[href]')

    def get_files(self):
        content = self.http_get(self.chapter)
        js = self.re.search(r'eval\((function\b.+)\((\'[\w ].+)\)\)', content).groups()
        data = self.re.search(r'\w=(\[.+\])', BaseLib.exec_js('m = ' + js[0], 'm(' + js[1] + ')')).group(1)
        data = self.json.loads(data.replace("'", '"'))
        n = self.http().normalize_uri
        return [n(i) for i in data]

    def get_cover(self):
        return self._cover_from_content('img.detail-info-cover-img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaFoxMe
