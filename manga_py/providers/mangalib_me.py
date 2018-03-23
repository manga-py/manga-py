from manga_py.provider import Provider
from .helpers.std import Std


class MangaLibMe(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = r'\.me/[^/]+/[^\d]+(\d+)/[^\d]+([^/]+)'
        idx = self.re.search(selector, self.chapter).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.me/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapters-list .chapter-item__name a')

    def get_files(self):
        content = self.http_get(self.chapter)
        base_url = self.re.search(r'\.scan-page.+src\'.+?\'([^\'"]+)\'', content).group(1)
        images = self.re.search(r'var\s+pages\s*=\s*(\[\{.+\}\])', content).group(1)
        imgs = ['{}/{}'.format(base_url, i.get('page_image')) for i in self.json.loads(images)]
        return imgs

    def get_cover(self):
        return self._cover_from_content('.topuserinfo-avatar > img')


main = MangaLibMe
