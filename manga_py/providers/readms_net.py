from manga_py.provider import Provider
from .helpers.std import Std


class ReadMsNet(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.re.search('/r/[^/]+/([^/]+)/([^/]+)', self.chapter).groups()
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/r/[^/]+/[^/]+/([^/]+)', self.chapter)
        return idx.group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.net/(?:manga|r)/([^/]+)')

    def get_chapters(self):
        return self._elements('.table-striped td > a')

    def get_files(self):
        img_selector = 'img#manga-page'
        parser = self.html_fromstring(self.chapter)
        img = self._images_helper(parser, img_selector)
        images = []
        img and images.append(img)
        pages = parser.cssselect('.btn-reader-page .dropdown-menu li + li a')
        for i in pages:
            parser = self.html_fromstring(self.http().normalize_uri(i.get('href')))
            img = self._images_helper(parser, img_selector)
            img and images.append(img)
        return images

    def get_cover(self):
        pass  # FIXME HOME

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ReadMsNet
