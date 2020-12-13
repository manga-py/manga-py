from manga_py.provider import Provider
from .helpers.std import Std


class MangaZukiMe(Provider, Std):
    _prefix = '/manga/'

    def get_chapter_index(self) -> str:
        try:
            re = self.re.compile(r'%s[^/]+/.+?(\d+(?:-\d+)?)[\?/]' % self._prefix)
            return re.search(self.chapter).group(1)
        except AttributeError:
            # mangazuki.online
            re = self.re.compile(r'%s[^/]+/.+?(\d+(?:-\d+)?)$' % self._prefix)
            return re.search(self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}%s{}' % self._prefix)

    def get_manga_name(self) -> str:
        return self._get_name('%s([^/]+)' % self._prefix)

    def get_chapters(self):
        chapters = []
        n = self.http().normalize_uri
        re = self.re.compile(r'(.+?)(?:\?style=list)?(?:/)?$')
        for ch in self._elements('.wp-manga-chapter > a'):
            href = re.search(ch.get('href')).group(1)
            chapters.append(n(href) + '?style=list')
        return chapters

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'img.wp-manga-chapter-img')

    def get_cover(self) -> str:
        image = self._cover_from_content('.summary_image > a > img', 'data-src')
        if len(image) < 1:
            # mangazuki.online
            image = self._cover_from_content('.summary_image > a > img')
        return image

    def prepare_cookies(self):
        self._prefix = self.re.search('(/mangas?/)', self.get_url()).group(1)

        self.cf_scrape(self.get_url())


main = MangaZukiMe
