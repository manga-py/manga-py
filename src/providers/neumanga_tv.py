from src.provider import Provider
from .helpers.std import Std


class NeuMangaTv(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        idx = self.re.search(r'/manga/[^/]+/(\d+(?:\+\d+))', chapter).group(1)
        return '-'.join(idx.split('+'))

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/manga/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        return self._elements('#scans .item-content a')

    def get_files(self):
        img_selector = '.imagechap'
        parser = self.html_fromstring(self.get_current_chapter())
        pages = self._first_select_options(parser, '.readnav select.page')
        images = self._images_helper(parser, img_selector)
        for i in pages:
            url = i.get('value').replace('//', '/').replace(':/', '://')
            images += self._images_helper(self.html_fromstring(url), img_selector)
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.info img.imagemg')


main = NeuMangaTv
