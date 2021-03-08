from manga_py.provider import Provider
from .helpers.std import Std


class ShakaiRu(Provider, Std):
    _api_url = 'http://shakai.ru/take/api-manga/request/shakai'

    def get_chapter_index(self) -> str:
        idx = self.chapter.get('data-first')
        return idx.replace('_', '-')

    def get_content(self):
        idx = self._get_name(r'/manga[^/]*/(\d+)')
        _ = {
            'dataRun': 'api-manga',
            'dataRequest': idx
        }
        with self.http().post(self._api_url, data=_) as resp:
            return resp.json()

    def get_manga_name(self) -> str:
        parser = self.content.get('post', [])
        idx = self._get_name(r'/manga[^/]*/(\d+)')
        parser = parser[3] if len(parser) > 3 else idx
        return parser.split('/')[0].strip()

    def get_chapters(self):
        return self.content.get('data', [])[::-1]

    def get_files(self):
        chapter = self.chapter
        if isinstance(chapter, dict):
            return chapter.get('data-second', [])
        return []

    def get_cover(self):
        pass  # FIXME HOME

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ShakaiRu
