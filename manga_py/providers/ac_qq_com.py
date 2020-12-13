from manga_py.crypt import AcQqComCrypt26, BaseLib
from manga_py.provider import Provider
from .helpers.std import Std


class AcQqCom(Provider, Std):
    _re = None

    def get_chapter_index(self) -> str:
        return self.re.search(r'/cid/(\d+)', self.chapter).group(1)

    def get_content(self):
        content = self._storage.get('main_content', None)
        if content is not None:
            return content
        idx = self._get_name(r'/id/(\d+)')
        return self.http_get('{}/Comic/comicInfo/id/{}'.format(self.domain, idx))

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.works-intro-title strong', 0)

    def get_chapters(self):
        return self._elements('.chapter-page-all li a')[::-1]

    def get_files(self):
        content = self.http_get(self.chapter)
        _nonce = self.re.search(r'window\[".*o.*c.*"\]\s*=\s*(.+);', content).group(1)
        _nonce = BaseLib.exec_js('var _P = {}'.format(_nonce), '_P')

        raw_data = self._re.search(content).group(1)

        data = AcQqComCrypt26.remap_content(_nonce, raw_data)
        data = AcQqComCrypt26.decode(data)

        json = self.json.loads(data)

        return [i['url'] for i in json.get('picture', [])]

    def get_cover(self) -> str:
        return self._cover_from_content('.works-cover img')

    def prepare_cookies(self):
        self._re = self.re.compile(r'var\s+DATA\s*=\s*[\'"](.*?)[\'"]')
        self._base_cookies()

    def book_meta(self) -> dict:
        result = {
            'author': self.text_content(self.content, '.works-intro-digi em'),
            'rating': self.text_content(self.content, 'p.ui-left strong'),
            'cover': self.get_cover(),
            'annotation': self.text_content(self.content, '.works-intro-short'),
            'language': 'cn',
        }

        return result


main = AcQqCom
