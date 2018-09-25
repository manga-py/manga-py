from manga_py.provider import Provider
from .helpers.std import Std


class WestMangaInfo(Provider, Std):
    _chapter_re = r'\.info/[^/]+-(\d+(?:-\d+)?)'

    def get_chapter_index(self) -> str:
        re = self.re.compile(self._chapter_re)
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/manga/'):
            return self._get_name('/manga/([^/]+)')
        url = self.html_fromstring(url, '.allc a', 0).get('href')
        self._params['url'] = self.http().normalize_uri(url)
        return self.get_manga_name()

    def get_chapters(self):
        # print(self.manga_name)
        return self._elements('span.leftoff > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.lexot img')

    def get_cover(self) -> str:
        return self._cover_from_content('.naru img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = WestMangaInfo
