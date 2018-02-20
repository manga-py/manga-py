from src.provider import Provider
from .helpers.std import Std
from urllib.parse import unquote_plus


class HitMangaEu(Provider, Std):
    _n = None
    postfix = None
    main_domain = 'http://www.mymanga.io'
    api_url = 'http://www.hitmanga.eu/listener/'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}'.format(idx)

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        idx = self.re.search('[^/]+/[^/]+/[^/]+?-([^/]+)', chapter)
        return idx.group(1)

    def get_main_content(self):
        url = '{}/mangas/{}/'.format(self.main_domain, self.get_manga_name())
        return self.content(url)

    def get_manga_name(self) -> str:
        url = self.get_url()
        re = '{}/([^/]+)'
        if url.find('/mangas/') > 0:
            re = '{}/mangas/([^/]+)'
        re = re.format(self.postfix)
        return self.re.search(re, url).group(1)

    def get_chapters(self):
        return self._chapters('.listchapseries li a.follow:not(.ddl)')

    def content(self, url):
        return self.re.sub(r'<!--.+?--!>', '', self.http_get(url))

    def get_files(self):
        chapter = self.get_current_chapter()
        img = self.document_fromstring(self.content(chapter), '#chpimg', 0).get('src')
        name = self.get_manga_name()
        idx = self.get_chapter_index()
        items = self.http_post(url=self.api_url, data={
            'number': unquote_plus(idx),
            'permalink': name,
            'type': 'chap-pages',
        })
        if items == '0':
            return []
        items = items.split('|')
        return [self._n(i, img) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('#picture img')

    def prepare_cookies(self):
        domain = self.get_domain().split('.')
        self.postfix = r'\.' + domain[-1]
        n = self.http().normalize_uri
        self._n = lambda u, r: n(u, r)


main = HitMangaEu
