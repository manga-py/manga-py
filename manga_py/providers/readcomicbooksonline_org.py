from manga_py.provider import Provider
from .helpers.std import Std


class ReadComicBooksOnlineOrg(Provider, Std):
    _name_re = r'\.(?:org|net)/(?:reader/)?([^/]+)'

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/reader/[^/]+/[^/]+_(\d+(?:[\./]\d+)?)', self.chapter)
        if not idx:
            idx = self.re.search(r'/reader/[^/]+_(\d+(?:[\./]\d+)?)', self.chapter)
        return '-'.join(self.re.split(r'[/\.]', idx.group(1)))

    def get_main_content(self):
        if ~self.get_url().find('/reader/'):
            _url = self.html_fromstring(self.get_url(), 'td .verse a', 0).get('href')
            self._params['url'] = _url
        return self.http_get('{}/{}'.format(self.domain, self._get_name(self._name_re)))

    def get_manga_name(self) -> str:
        return self._get_name(self._name_re)

    def get_chapters(self):
        return self._elements('#chapterlist .chapter > a')

    def prepare_cookies(self):
        self._storage['domain_uri'] = self.domain.replace('/www.', '/')

    def _get_image(self, parser):
        src = parser.cssselect()
        if not src:
            return None
        return '{}/reader/{}'.format(self.domain, src[0].get('src'))

    def get_files(self):
        parser = self.html_fromstring(self.chapter + '?q=fullchapter')
        base = parser.cssselect('base')
        if base is not None and len(base):
            base = base[0].get('href')
        else:
            base = None
        n = self.http().normalize_uri
        return [n(i, base) for i in self._images_helper(parser, '#omv td > img')]

    def get_cover(self):
        self._cover_from_content(self.content, '.pic > img.series')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ReadComicBooksOnlineOrg
