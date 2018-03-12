from src.provider import Provider
from .helpers.std import Std


class AuthroneCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.re.search('/manga/[^/]+/([^/]+/[^/]+)', self.chapter).group(1).split('.', 2)
        if len(idx) > 1:
            return 'vol_{:0>3}-{}_{}'.format(idx[0], *idx[1].split('/'))
        return 'vol_{:0>3}-0-{}'.format(*idx[0].split('/'))

    def get_chapter_index(self) -> str:
        return self.re.search('/manga/[^/]+/([^/]+)', self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):  # need sorting chapters: /manga/love_stage/
        ch_selector = '.mng_det ul.lst > li > a'
        items = self._elements(ch_selector)
        pages = self._elements('ul.lst + ul.pgg li:last-child > a')
        patern = r'list/(\d+)/'
        if pages and len(pages):
            link = pages[-1].get('href')
            page = self.re.search(patern, link).group(1)
            for i in range(2, int(page) + 1):
                page_link = self.re.sub(patern, 'list/%d/' % i, link)
                items += self._elements(ch_selector, self.http_get(page_link))
        return items

    def _get_image(self, parser):
        img = parser.cssselect('.prw > a > img')
        if not img:
            return []
        img = img[0].get('src')
        img = self.re.sub(r'\w\.mhcdn', 'c.mhcdn', img)  # only C cnd working now!
        return [img]

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        pages = self._first_select_options(parser, 'select.cbo_wpm_pag')
        images = self._get_image(parser)
        for i in pages:
            parser = self.html_fromstring(self.chapter + i.get('value') + '/')
            images += self._get_image(parser)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('#sct_content img.cvr')


main = AuthroneCom
