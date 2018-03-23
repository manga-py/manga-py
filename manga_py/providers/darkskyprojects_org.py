from manga_py.provider import Provider
from .helpers.std import Std


class DarkSkyProjectsOrg(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}-{}'.format(
            self.chapter_id,
            self.get_chapter_index()
        )

    def get_chapter_index(self) -> str:
        ch = self.chapter
        return self.re.search('/biblioteca/[^/]+/([^/]+)', ch).group(1)

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


main = DarkSkyProjectsOrg
