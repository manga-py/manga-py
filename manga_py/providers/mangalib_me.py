from manga_py.provider import Provider
from .helpers.std import Std


class MangaLibMe(Provider, Std):

    def get_chapter_index(self) -> str:
        selector = r'\.\w{2,7}/[^/]+/[^\d]+(\d+)/[^\d]+([^/]+)'
        idx = self.re.search(selector, self.chapter).groups()
        return '-'.join(idx)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapters-list .chapter-item__name a')

    def get_files(self):
        content = self.http_get(self.chapter)
        images = self.re.search(r'__pg\s*=\s*(\[.+\])', content).group(1)
        info = self.re.search(r'__info\s*=\s*(\{.+\})', content).group(1)
        images = self.json.loads(images)
        info = self.json.loads(info)
        _manga = info['img']['url']
        _s = info['servers']
        _server = _s.get('main', _s.get('secondary'))

        return ['{}{}{}'.format(_server, _manga, i['u']) for i in images]

    def get_cover(self):
        return self._cover_from_content('img.manga__cover')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaLibMe
