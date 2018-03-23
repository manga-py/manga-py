from manga_py.provider import Provider
from .helpers.std import Std


class ZingBoxMe(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}'.format(idx)

    def get_chapter_index(self) -> str:
        return str(self.chapter.get('title', '0'))

    def get_main_content(self):
        idx = self.re.search('/manga/(?:[^/]+/)?(\d+)/', self.get_url())
        _ = {
            'url': '/manga/getBookDetail/{}'.format(idx.group(1)),
            'method': 'GET',
            'api': '/mangaheatapi/web',
        }
        return self.http_post(self.domain + '/api', data=_)

    def get_manga_name(self) -> str:
        return self._get_name(r'\.me/manga/(?:\d+/)?([^/]+)')

    def get_chapters(self):
        try:
            return self.json.loads(self.content).get('child', [])
        except self.json.JSONDecodeError:
            return []

    def get_files(self):
        idx = self.chapter.get('chapterId', 0)
        _ = {
            'url': '/manga/getChapterImages/{}'.format(idx),
            'method': 'GET',
            'api': '/mangaheatapi/web',
        }
        images = self.http_post(self.domain + '/api', data=_)
        return self.json.loads(images).get('images', [])

    def get_cover(self):
        return self._cover_from_content('.comicImg img')


main = ZingBoxMe
