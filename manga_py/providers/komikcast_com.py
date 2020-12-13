from manga_py.provider import Provider
from .helpers.std import Std


class KomikCastCom(Provider, Std):
    def get_chapter_index(self) -> str:
        re = self.re.compile(r'-chapter-(\d+(?:-\d+)?)')
        return re.search(self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/chapter/'):
            url = self.html_fromstring(url, '.allc a', 0).get('href')
            self._params['url'] = self.http().normalize_uri(url)
            return self.get_manga_name()
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self) -> list:
        return self._elements('.mangainfo .leftoff a')

    def get_files(self) -> list:
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#readerarea img')

    def get_cover(self):
        return self._cover_from_content('.topinfo img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = KomikCastCom
