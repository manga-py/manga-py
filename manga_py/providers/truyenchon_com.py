from manga_py.provider import Provider
from .helpers.std import Std


class TruyenChonCom(Provider, Std):
    __subtype = None

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/chap.*?-(\d+(?:\.\d+)?)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_main_content(self):
        truyen = 'truyen'
        if ~self.domain.find('nettruyen.'):
            truyen = 'truyen-tranh'
        return self._get_content('{}/%s/{}' % truyen)

    def get_manga_name(self) -> str:
        groups = self.re.search(r'/(truyen.*?)/([^/]+)', self.get_url())
        self.__subtype = groups.group(1)
        return groups.group(2)

    def get_chapters(self):
        return self._elements('.list-chapter .chapter > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.page-chapter > img', 'data-original')

    def get_cover(self) -> str:
        return self._cover_from_content('.col-image > img')

    def book_meta(self) -> dict:
        pass


main = TruyenChonCom
