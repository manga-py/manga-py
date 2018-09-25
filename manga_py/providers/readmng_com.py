from manga_py.provider import Provider
from .helpers.std import Std


class ReadMngCom(Provider, Std):

    def get_chapter_index(self) -> str:
        ch = self.chapter
        re = r'\.com/[^/]+/(\d+(?:\.\d+)?)/?'
        idx = self.re.search(re, ch)
        if not idx:
            return self.re.search(r'\.com/[^/]+/([^/]+)', ch).group(1)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        return self._elements('.chp_lst li > a')

    def get_files(self):
        url = self.chapter + '/all-pages'
        parser = self.html_fromstring(url)
        return self._images_helper(parser, '.content-list img.img-responsive')

    def get_cover(self) -> str:
        return self._cover_from_content('.panel-body img.img-responsive')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ReadMngCom
