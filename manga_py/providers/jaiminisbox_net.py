from manga_py.provider import Provider
from .helpers.std import Std


class JaiminisBoxNet(Provider, Std):
    _manga_idx = None
    _re = None

    def get_chapter_index(self) -> str:
        return self._re.search(self.chapter).group(1)

    def get_content(self):
        content = self._get_content('{}/manga/{}')
        self.__set_idx(content)
        return content

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga/([^/]+)/')

    def get_chapters(self):
        if self._manga_idx is None:
            return []

        content = self.http_post(
            'https://jaiminisbox.net/wp-admin/admin-ajax.php',
            data={
                'action': 'manga_get_chapters',
                'manga': self._manga_idx,
            }
        )

        return self._elements(
            '.listing-chapters_wrap .wp-manga-chapter > a',
            content
        )

    def get_files(self):
        return self._images_helper(
            self.html_fromstring(self.chapter),
            '.reading-content img.wp-manga-chapter-img',
        )

    def get_cover(self) -> str:
        return self._cover_from_content('.summary_image > a > img')

    def prepare_cookies(self):
        self._re = self.re.compile(r'/chapter-(\d+)/')

    def __set_idx(self, content):
        parser = self.document_fromstring(content, 'input.rating-post-id', 0)
        if parser is not None:
            self._manga_idx = int(parser.get('value'))


main = JaiminisBoxNet
