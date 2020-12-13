from manga_py.provider import Provider
from .helpers.std import Std


class PururinIo(Provider, Std):

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_content(self):
        url = self.get_url()
        if ~url.find('/gallery/'):
            re = r'/gallery/(\d+)/([^/]+)'
        else:
            re = r'/read/(\d+)/\d+/([^/]+)'
        return self._get_content('{}/gallery/{}/{}'.format(
            self.domain,
            *self.re.search(re, url).groups()
        ))

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/gallery/'):
            re = r'/gallery/\d+/([^/]+)'
        else:
            re = r'/read/\d+/\d+/([^/]+)'
        return self._get_name(re)

    def get_chapters(self):
        return [b'']

    def _images(self, content):
        items = self.json.loads(content)
        images = []
        for i in items:
            url = items.get(i, {}).get('image', False)
            url and images.append(url)
        return images

    def get_files(self):
        items = self._elements('.col-md-10 .well-pururin > div[class*="preview"] > a')
        if items:
            url = self.http().normalize_uri(items[0].get('href'))
            content = self.http_get(url)
            images = self.re.search(r'chapters\s*=\s*(\{.+\})\s*;', content)
            if images:
                return self._images(images.group(1))
        return []

    def get_cover(self) -> str:
        return self._cover_from_content('.cover > a > img')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = PururinIo
