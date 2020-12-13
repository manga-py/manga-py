from manga_py.provider import Provider
from .helpers.std import Std


class ZeroScansCom(Provider, Std):
    _key = '/comics/'

    def get_chapter_index(self) -> str:
        return self.re.search(
            r'%s[^/]+/(\d+/\d+)' % self._key,
            self.chapter
        ).group(1).replace('/', '-')

    def get_content(self):
        name = self._get_name(r'%s([^/]+)' % self._key)
        return self.http_get('%s%s%s/' % (
            self.domain,
            self._key,
            name
        ))

    def get_manga_name(self) -> str:
        return self._get_name(r'%s\d+-([^/]+)' % self._key)

    def get_chapters(self):
        return self._elements('.list .list-item a.text-color')

    def get_files(self):
        content = self.http_get(self.chapter)
        raw_images = self.re.search(
            r'chapterPages\s?=\s?(\[.+?\])',
            content
        ).group(1)
        images = self.json.loads(raw_images)

        n = self.http().normalize_uri

        return [n(i) for i in images]

    def get_cover(self) -> str:
        image = self._elements('.media img.media-content')
        if len(image):
            return self.parse_background(image)
        return ''


main = ZeroScansCom
