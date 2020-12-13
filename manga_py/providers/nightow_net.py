from urllib.parse import unquote_plus

from manga_py.provider import Provider
from .helpers.std import Std


class NightowNet(Provider, Std):
    _name_re = r'manga=(.+?)(?:&.+)?$'

    def get_chapter_index(self) -> str:
        ch = unquote_plus(self.chapter)
        idx = self.re.search(r'chapter=(?:.+?)\+(\d+(?:\.\d+)?)', ch)
        if idx:
            return '-'.join(idx.group(1).split('.'))
        return self.re.search('chapter=(.+?)(?:&.+)?$', ch).group(1)

    def get_content(self):
        name = self._get_name(self._name_re)
        return self.http_get('{}/online/?manga={}'.format(
            self.domain,
            name
        ))

    def get_manga_name(self) -> str:
        return unquote_plus(self._get_name(self._name_re))

    def get_chapters(self):
        return self._elements('.selector .options a')

    def prepare_cookies(self):
        self._storage['referer'] = self.domain + '/online/'

    def get_files(self):
        content = self.http_get(self.chapter)
        items = self.re.findall(r'imageArray\[\d+\]\s*=\s*[\'"](.+)[\'"];', content)
        n = self.http().normalize_uri
        return [n(i) for i in items]

    def get_cover(self) -> str:
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass


main = NightowNet
