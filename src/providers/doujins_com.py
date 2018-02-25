from src.provider import Provider
from .helpers.std import Std


class DoujinsCom(Provider, Std):
    img_selector = '#image-container img.doujin'

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        return self._get_name('/gallery/([^/]+)')

    def get_chapters(self):
        return [self.get_url()]

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), self.img_selector)
        return [i.get('data-file').replace('&amp;', '&') for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content(self.img_selector)


main = DoujinsCom
