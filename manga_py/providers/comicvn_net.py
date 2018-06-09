from manga_py.provider import Provider
from .helpers.std import Std


class ComicNnNet(Provider, Std):

    def get_archive_name(self) -> str:
        return self.get_chapter_index()

    def get_chapter_index(self) -> str:  # todo
        re = self.re.compile('/truyen-tranh-online/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/truyen-tranh-online/{}')

    def _iframe_hook(self, url):
        content = self.html_fromstring(url)
        iframe = content.cssselect('iframe')
        if iframe:
            url = iframe[0].get('src')
            print('Iframe!\n' + url)
        return self.html_fromstring(url)

    def get_manga_name(self) -> str:
        name = self._get_name(r'/truyen-tranh-online/([^/]+)')
        if self.re.search('.+-\d+', name):
            return name
        a = self._iframe_hook(self.get_url())
        self._params['url'] = a.cssselect('.sub-bor h1 a')[0].get('href')
        return self.get_manga_name()

    def get_chapters(self):
        return self._elements('.manga-chapter-head + ul li > a')

    def get_files(self):
        content = self._iframe_hook(self.chapter)
        files = content.cssselect('textarea#txtarea img')
        if files:
            n = self.http().normalize_uri
            return [n(i.get('src')) for i in files]
        return []

    def prepare_cookies(self):
        self._base_cookies()

    def get_cover(self) -> str:
        return self._cover_from_content('.manga-detail .row img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ComicNnNet
