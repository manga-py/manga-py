from manga_py.provider import Provider
from .helpers.std import Std
from urllib import parse


class ComicPunchNet(Provider, Std):

    def get_chapter_index(self) -> str:
        return self.re.search(r'[-/]((?:Annual|Issue|Chapter)-\w+)', self.chapter).group(1)

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.page-title')

    def get_chapters(self):
        return self._elements('.chapter > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter + '?q=fullchapter')
        base_url = parser.cssselect('base[href]')[0].get('href')
        return [parse.urljoin(base_url, i) for i in self._images_helper(parser, 'img.picture')]

    def get_cover(self) -> str:
        return self._cover_from_content('.pic .series')


main = ComicPunchNet
