from manga_py.provider import Provider
from .helpers.std import Std


class VizCom(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.chapter_id)

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        url = self.re.search('/([^/]+/chapters/[^/]+)').group(1)
        return self.http_get('{}/{}'.format(self.domain, url))

    def get_manga_name(self) -> str:
        return self._get_name('/chapters/([^/]+)')

    def get_chapters(self):
        pass

    def get_files(self):
        pass

    def get_cover(self):
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass

    def prepare_cookies(self):
        pass


main = VizCom
