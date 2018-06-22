from manga_py.provider import Provider
from .helpers.std import Std


class ChoChoxCom(Provider, Std):

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        return [b'']

    def get_files(self):
        return [i.get('src') for i in self._elements('img.alignnone')]

    def get_cover(self) -> str:
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = ChoChoxCom
