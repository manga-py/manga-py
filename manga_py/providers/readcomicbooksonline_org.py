from manga_py.provider import Provider
from .helpers.std import Std


class ReadComicBooksOnlineOrg(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/reader/[^/]+/[^/]+_(\d+(?:[\./]\d+)?)', self.chapter)
        if not idx:
            idx = self.re.search(r'/reader/[^/]+_(\d+(?:[\./]\d+)?)', self.chapter)
        return '-'.join(self.re.split(r'[/\.]', idx.group(1)))

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.(?:org|net)/(?:reader/)?([^/]+)')

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
        n = self.http().normalize_uri
        print([n(i) for i in self._images_helper(parser, '#omv td > img')])
        print('')
        print(['{}/reader/{}'.format(self.domain, i) for i in self._images_helper(parser, '#omv td > img')])
        exit()
        return [self.chapter + i for i in self._images_helper(parser, '#omv td > img')]

    def get_cover(self):
        self._cover_from_content(self.content, '.pic > img.series')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ReadComicBooksOnlineOrg
