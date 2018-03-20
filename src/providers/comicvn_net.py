from src.provider import Provider
from .helpers.std import Std


class ComicNnNet(Provider, Std):

    def get_archive_name(self) -> str:
        return self.get_chapter_index()

    def get_chapter_index(self) -> str:
        re = self.re.compile('/truyen-tranh-online/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/truyen-tranh-online/{}')

    def _iframe_hook(self, url):
        content = self.html_fromstring(self.get_url())
        iframe = content.cssselect('iframe')
        url = self.get_url()
        if iframe:
            print('Iframe!')
            url = iframe[0].get('src')
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
        files = content.cssselect('textarea#txtarea')
        print(len(files))
        if files:
            return self._elements('img', files[0].text_content())
        return []

    def prepare_cookies(self):
        self._base_cookies()

    def get_cover(self) -> str:
        return self._cover_from_content('.manga-detail .row img')


main = ComicNnNet
