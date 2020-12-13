from manga_py.provider import Provider
from .helpers.std import Std


class HentaiImageCom(Provider, Std):

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_content(self):
        return self._get_content('{}/image/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/image/([^/]+)')

    def get_chapters(self):
        return [b'']

    def _pages(self, parser):
        pages = parser.cssselect('#paginator')
        if pages:
            href = pages[0].cssselect('span > a')[-1].get('href')
            page = self.re.search(r'/page/(\d+)', href)
            return range(2, int(page.group(1)) + 1)
        return []

    def get_files(self):
        parser = self.document_fromstring(self.content)
        pages = self._pages(parser)
        selector = '#display_image_detail div > a > img'
        images = self._images_helper(parser, selector)
        for i in pages:
            content = self._get_content('{}/image/{}/page/%d' % i)
            parser = self.document_fromstring(content)
            images += self._images_helper(parser, selector)
        return images

    def get_cover(self) -> str:
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = HentaiImageCom
