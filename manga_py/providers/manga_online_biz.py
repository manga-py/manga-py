from manga_py.fs import get_temp_path, rename, path_join, dirname
from manga_py.provider import Provider
from .helpers.std import Std, Http2


# Archive downloading example. Without images
class MangaOnlineBiz(Provider, Std):
    chapter_url = ''
    _idx = 0

    def get_chapter_index(self) -> str:
        url = self._storage['chapters'][self._idx]
        idx = self.re.search(r'/download/[^/]+/.+?_(\d+)_(\d+)', url).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        return self._get_content('{}/{}.html')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.biz/([^/]+)(?:/|\.html)')

    def _after_download(self, idx, _path):
        self._idx = idx + 1

    def loop_chapters(self):
        http2 = Http2(self)
        http2.download_archives(self._storage['chapters'])
        http2.after_download = self._after_download

    def get_chapters(self):
        s, c = r'MangaChapter\((.+)\);', self.content
        items = self.json.loads(self.re.search(s, c).group(1))
        return [i.get('downloadUrl') for i in items]

    def get_files(self):
        return []

    def get_cover(self):
        return self._cover_from_content('.item > .image > img')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.chapter_url


main = MangaOnlineBiz
