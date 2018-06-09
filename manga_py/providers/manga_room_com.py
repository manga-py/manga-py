from manga_py.provider import Provider
from .helpers.std import Std


class MangaRoomCom(Provider, Std):

    def get_archive_name(self) -> str:  # fixme! #49
        idx = self.get_chapter_index().split('-')
        if len(idx) > 1:
            return '{}vol_{:0>3}'.format(*idx)
        return 'vol_{:0>3}'.format(idx[0])

    def get_chapter_index(self) -> str:
        re = self.re.search(r'version-(\d+)', self.chapter)
        version = ''
        if re:
            version = '-' + re.group(1)
        re = self.re.search(r'chapter-(\d+)', self.chapter)
        return '{}{}'.format(version, re.group(1))

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        # : downloaded all versions
        return ['{}/manga/{}'.format(
            self.domain, i.get('href')
        ) for i in self._elements('.chapter-list a')]

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#main_div .lazy_image_page')

    def get_cover(self) -> str:
        return self._cover_from_content('img#manga_thumps')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaRoomCom
