from manga_py.provider import Provider
from .helpers.std import Std


class DarkSkyProjectsOrg(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name({'vol': [
            self.chapter_id,
            self.get_chapter_index()
        ]})

    def get_chapter_index(self) -> str:
        return self.re.search('/biblioteca/[^/]+/([^/]+)', self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/biblioteca/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/biblioteca/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapters h5 a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'data-src')

    def get_cover(self) -> str:
        return self._cover_from_content('.boxed > .img-responsive')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = DarkSkyProjectsOrg
