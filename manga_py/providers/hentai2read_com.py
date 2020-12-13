from manga_py.provider import Provider
from .helpers.std import Std


class Hentai2ReadCom(Provider, Std):
    images_cdn = 'https://static.hentaicdn.com/hentai'

    def get_chapter_index(self) -> str:
        idx = self.re.search('.+/([^/]+)/', self.chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)')

    def get_chapters(self):
        return self._elements('li .media > a')

    def get_files(self):
        content = self.http_get(self.chapter)
        selector = r'\'images\'\s*:\s*(\[.+\])'
        items = self.json.loads(self.re.search(selector, content).group(1))
        return ['{}{}'.format(self.images_cdn, i) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.ribbon-primary a > img')


main = Hentai2ReadCom
