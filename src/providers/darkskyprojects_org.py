from src.provider import Provider
from .helpers.std import Std


class DarkSkyProjectsOrg(Provider, Std):

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        pass

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        return self._get_name('/biblioteca/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapters h5 a')

    def get_files(self):
        return []

    def get_cover(self) -> str:
        return self._cover_from_content('.boxed > .img-responsive')


main = DarkSkyProjectsOrg
