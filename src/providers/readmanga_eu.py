from src.provider import Provider
from .helpers.std import Std


class ReadMangaEu(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx, '1'))

    def get_chapter_index(self) -> str:
        idx = self.re.search('/manga/\d+/[^/]+/([^/]+)', self.get_current_chapter())
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        name = self.re.search('/(manga/\d+/[^/]+)', self.get_url()).group(1)
        return self.http_get('{}/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/manga/\d+/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        selector = '#chapters_b a[href*="/manga/"]'
        return self.document_fromstring(self.get_storage_content(), selector)

    def parse_files(self, parser):
        images_class = '.mainContent img.ebook_img'
        images = []
        for i in parser.cssselect(images_class):
            images.append(self.http().normalize_uri(i.get('src')))
        return images

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        pages = parser.cssselect('#jumpto > option + option')
        images = self.parse_files(parser)
        for i in pages:
            url = self.http().normalize_uri(i.get('value'))
            parser = self.html_fromstring(url)
            images += self.parse_files(parser)
        return images

    def get_cover(self):
        pass  # TODO


main = ReadMangaEu
