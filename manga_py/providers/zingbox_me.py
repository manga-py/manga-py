from manga_py.provider import Provider
from .helpers.std import Std


class ZingBoxMe(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        return str(self.chapter.get('title', '0'))

    def get_content(self):
        idx = self.re.search(r'/manga/(?:[^/]+/)?(\d+)/', self.get_url())
        data = {
            'url': '/manga/getBookDetail/{}'.format(idx.group(1)),
            'method': 'GET',
            'api': '/mangaheatapi/web',
        }
        with self.http().post(self.domain + '/api', data=data) as resp:
            return resp.json()

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/manga/(?:\d+/)?([^/]+)')

    def get_chapters(self):
        return self.content.get('child', [])

    def _chapter_url(self):
        idx = self.chapter.get('chapterId', 0)
        return '/manga/getChapterImages/{}'.format(idx)

    def get_files(self):
        data = {
            'url': self._chapter_url(),
            'method': 'GET',
            'api': '/mangaheatapi/web',
        }
        with self.http().post(self.domain + '/api', data=data) as resp:
            return resp.json().get('images', [])

    def get_cover(self):
        return self._cover_from_content('.comicImg img')

    def chapter_for_json(self):
        return self._chapter_url()


main = ZingBoxMe
