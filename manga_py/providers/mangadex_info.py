from manga_py.provider import Provider
from .helpers.std import Std


class MangaDexCom(Provider, Std):
    _content = None

    def get_chapter_index(self) -> str:
        return self.re.search(r'-chapter-(\d+(?:\.\d+)?)', self.chapter).group(1).replace('.', '-')

    def get_main_content(self):
        if self._content is None:
            self._content = self.http_get(self.get_url())
        return  self._content

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.info-title')

    def get_chapters(self):
        return self._elements('.widget .table.table-striped td > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter + '/0')
        self.http().referer = ''
        return self._images_helper(parser, '#view-chapter img')

    def get_cover(self) -> str:
        return self._cover_from_content('.img-thumbnail')

    def prepare_cookies(self):
        self.http().allow_send_referer = False


main = MangaDexCom
