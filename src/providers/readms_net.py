from src.provider import Provider
from .helpers.std import Std


class ReadMsNet(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.re.search('/r/[^/]+/([^/]+)/([^/]+)', self.get_current_chapter()).groups()
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/r/[^/]+/[^/]+/([^/]+)', self.get_current_chapter())
        return '{}'.format(idx.group(1))

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search(r'\.net/(?:manga|r)/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        return self.document_fromstring(self.get_storage_content(), '.table-striped td > a')

    def get_files(self):
        img_selector = 'img#manga-page'
        parser = self.html_fromstring(self.get_current_chapter())
        img = self._images_helper(parser, img_selector)
        images = []
        img and images.append(img)
        pages = parser.cssselect('.btn-reader-page .dropdown-menu li + li a')
        for i in pages:
            parser = self.html_fromstring(self.http().normalize_uri(i.get('href')))
            img = self._images_helper(parser, img_selector)
            img and images.append(img)
        return images


main = ReadMsNet
