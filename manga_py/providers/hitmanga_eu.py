from urllib.parse import unquote_plus

from manga_py.provider import Provider
from .helpers.std import Std


class HitMangaEu(Provider, Std):
    _n = None
    postfix = None
    main_domain = 'http://www.mymanga.io'
    api_url = 'http://www.hitmanga.eu/listener/'

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        idx = self.re.search('[^/]+/[^/]+/[^/]+?-([^/]+)', chapter)
        return idx.group(1)

    def get_content(self):
        return self._content(self._get_content('{}/mangas/{}/'))

    def get_manga_name(self) -> str:
        url = self.get_url()
        re = '{}/([^/]+)'
        if ~url.find('/mangas/'):
            re = '{}/mangas/([^/]+)'
        re = re.format(self.postfix)
        return self.re.search(re, url).group(1)

    def get_chapters(self):
        return self._elements('.listchapseries li a.follow:not(.ddl)')

    def _content(self, url):
        return self.re.sub(r'<!--.+?--!>', '', self.http_get(url))

    def get_files(self):
        chapter = self.chapter
        img = self.document_fromstring(self._content(chapter), '#chpimg', 0).get('src')
        idx = self.get_chapter_index()
        items = self.http_post(url=self.api_url, data={
            'number': unquote_plus(idx),
            'permalink': self.manga_name,
            'type': 'chap-pages',
        })
        if items == '0':
            return []
        items = items.split('|')
        return [self._n(i, img) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('#picture img')

    def prepare_cookies(self):
        domain = self.domain.split('.')
        self.postfix = r'\.' + domain[-1]
        n = self.http().normalize_uri
        self._n = lambda u, r: n(u, r)

    def book_meta(self) -> dict:
        # todo meta
        pass


main = HitMangaEu
