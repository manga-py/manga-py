from manga_py.provider import Provider
from .helpers.std import Std


class ZingBoxMe(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        return str(self.chapter.get('title', '0'))

    def get_main_content(self):
        idx = self.re.search('/manga/(?:[^/]+/)?(\d+)/', self.get_url())
        data = {
            'url': '/manga/getBookDetail/{}'.format(idx.group(1)),
            'method': 'GET',
            'api': '/mangaheatapi/web',
        }
        return self.http_post(self.domain + '/api', data=data)

    def get_manga_name(self) -> str:
        return self._get_name(r'\.me/manga/(?:\d+/)?([^/]+)')

    def get_chapters(self):
        try:
            return self.json.loads(self.content).get('child', [])
        except self.json.JSONDecodeError:
            return []

    def _chapter_url(self):
        idx = self.chapter.get('chapterId', 0)
        return '/manga/getChapterImages/{}'.format(idx)

    def get_files(self):
        _ = {
            'url': self._chapter_url(),
            'method': 'GET',
            'api': '/mangaheatapi/web',
        }
        images = self.http_post(self.domain + '/api', data=_)
        return self.json.loads(images).get('images', [])

    def get_cover(self):
        return self._cover_from_content('.comicImg img')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self._chapter_url()


main = ZingBoxMe
