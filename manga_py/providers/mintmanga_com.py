from .helpers.std import Std
from .readmanga_me import ReadmangaMe


class MintMangaCom(ReadmangaMe, Std):

    def get_manga_name(self):
        return self._get_name(r'\.com/([^/]+)')


main = MintMangaCom
