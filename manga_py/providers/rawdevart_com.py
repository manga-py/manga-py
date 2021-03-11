from manga_py.provider import Provider
from .helpers.std import Std


class RawDevArtCom(Provider, Std):
    def get_chapter_index(self) -> str:
        return self.re.search(r'/chapter-(\d+(?:-\d+)?)', self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/comic/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'/comic/([^/]+)')

    def get_chapters(self):
        chapters = []
        chapters += self._elements('.list-group-item > a', self.content)

        for page in self.pages():
            url = '{}/comic/{}/?page={}'.format(self.domain, self.manga_name, page)
            chapters += self._elements('.list-group-item > a', self.http_get(url))

        return chapters

    def pages(self):
        pages = self._elements('.pagination .page-item > a')

        try:
            max_page = self.re.search(r'page=(\d+)', pages[-1].get('href')).group(1)
            return map(str, range(2, 1 + int(max_page)))
        except IndexError:
            return []

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'img.img-fluid', 'data-src', 'src')

    def get_cover(self) -> str:
        parser = self.document_fromstring(self.content)
        return self._images_helper(parser, 'img.img-fluid')[0]


main = RawDevArtCom
