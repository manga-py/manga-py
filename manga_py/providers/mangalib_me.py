from manga_py.provider import Provider
from .helpers.std import Std


class MangaLibMe(Provider, Std):

    def get_chapter_index(self) -> str:
        selector = r'\.me/[^/]+/[^\d]+(\d+)/[^\d]+([^/]+)'
        idx = self.re.search(selector, self.chapter).groups()
        return '-'.join(idx)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.me/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapters-list .chapter-item__name a')

    def get_files(self):
        content = self.http_get(self.chapter)
        base_url = self.re.search(r'\bimgUrl: *[\'"]([^\'"]+)', content).group(1)
        images = self.re.search(r'\bpages: *(\[\{.+\}\])', content).group(1)
        images = self.json.loads(images)
        imgs = ['https://img2.mangalib.me{}{}'.format(
            base_url,
            i.get('page_image'),
        ) for i in images]
        return imgs

    def get_cover(self):
        return self._cover_from_content('img.manga__cover')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaLibMe
