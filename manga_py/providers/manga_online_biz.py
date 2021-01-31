
from manga_py.provider import Provider
from manga_py.download_methods import WholeArchiveDownloader
from .helpers.std import Std

# Archive downloading example. Without images
class MangaOnlineBiz(Provider, Std):
    _downloader = WholeArchiveDownloader
    chapter_url = ''

    def get_chapter_index(self) -> str:
        url = self.chapter
        idx = self.re.search(r'/download/[^/]+/.+?_(\d+)_(\d+)', url).groups()
        return '{}-{}'.format(*idx)

    def get_content(self):
        return self._get_content('{}/{}.html')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)(?:/|\.html)')

    def _after_download(self, idx, _path):
        self._idx = idx + 1

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
