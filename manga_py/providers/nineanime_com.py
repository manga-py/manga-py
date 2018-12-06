from manga_py.provider import Provider
from .helpers.std import Std


class NineAnimeCom(Provider, Std):
    _ch = None

    def get_chapter_index(self) -> str:
        ch_result = self._ch.search(self.chapter)
        if ch_result:
            return ch_result.group(1).replace('_', '-')
        return '000-' + self.chapter_id

    def get_main_content(self):
        return self._get_content('{}/manga/{}.html?waring=1')

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga/(.+)\.html')

    def get_chapters(self):
        return self._elements('.detail-chlist a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter.rstrip('/') + '-0-1.html')
        return self._images_helper(parser, 'img.manga_pic')

    def get_cover(self) -> str:
        return self._cover_from_content('img.detail-cover')

    def book_meta(self) -> dict:
        pass

    def prepare_cookies(self):
        self._ch = self.re.compile(r'/chapter/.*?(?:_((?:\d+)(?:_\d+)?))[^/]*?[/]')


main = NineAnimeCom
