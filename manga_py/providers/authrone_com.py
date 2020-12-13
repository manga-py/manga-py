from .helpers.std import Std
from .mangaonline_today import MangaOnlineToday


class AuthroneCom(MangaOnlineToday, Std):
    _ch_selector = '.mng_det ul.lst > li > a'

    def get_archive_name(self) -> str:
        idx = self.re.search('/manga/[^/]+/([^/]+/[^/]+)', self.chapter).group(1).split('.', 2)
        if len(idx) > 1:
            return 'vol_{:0>3}-{}_{}'.format(idx[0], *idx[1].split('/'))
        return 'vol_{:0>3}-0-{}'.format(*idx[0].split('/'))

    def get_chapter_index(self) -> str:
        return self.re.search('/manga/[^/]+/([^/]+)', self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):  # need sorting chapters: /manga/love_stage/
        items = self._elements(self._ch_selector)
        pages = self._elements('ul.lst + ul.pgg li:last-child > a')
        patern = r'list/(\d+)/'
        if pages and len(pages):
            link = pages[-1].get('href')
            page = self.re.search(patern, link).group(1)
            for i in range(2, int(page) + 1):
                page_link = self.re.sub(patern, 'list/%d/' % i, link)
                items += self._elements(self._ch_selector, self.http_get(page_link))
        return items

    def get_cover(self) -> str:
        return self._cover_from_content('#sct_content img.cvr')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = AuthroneCom
