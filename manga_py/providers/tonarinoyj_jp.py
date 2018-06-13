from manga_py.provider import Provider
from .helpers import tonarinoyj_jp
from .helpers.std import Std


class TonariNoYjJp(Provider, Std):
    helper = None

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        content = self._storage.get('main_content', None)
        if content is None:
            return self.http_get(self.get_url())
        return content

    def get_manga_name(self) -> str:
        h1 = self.document_fromstring(self.content, 'h1.series-header-title')
        if h1:
            return h1[0].text_content()
        return '__Manga__'

    def get_chapters(self):
        idx = self.re.search(r'/episode/(\d+)', self.get_url())
        items = self.helper.get_chapters(idx.group(1))
        return ['{}/episode/{}'.format(self.domain, i) for i in items]

    def get_files(self):
        doc = self.html_fromstring(self.chapter)
        images = []
        # img = doc.cssselect('.link-slot > img')  # sometimes 1x1 px
        # img and images.append(img[0].get('src'))
        images += [i.get('data-src') for i in doc.cssselect('img.js-page-image')]
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.link-slot > img')

    def prepare_cookies(self):
        self.helper = tonarinoyj_jp.TonariNoYjJp(self)

    def after_file_save(self, _path: str, idx: int):
        if idx:
            self.helper.solve_image(_path, idx)

    def book_meta(self) -> dict:
        # todo meta
        pass


main = TonariNoYjJp
