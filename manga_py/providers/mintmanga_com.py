from .readmanga_me import ReadmangaMe
from .helpers.std import Std


class MintMangaCom(ReadmangaMe, Std):

    def get_manga_name(self):
        return self._get_name(r'\.com/([^/]+)')


main = MintMangaCom
