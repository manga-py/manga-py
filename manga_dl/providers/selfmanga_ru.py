from .readmanga_me import ReadmangaMe


class SelfMangaRu(ReadmangaMe):

    def get_manga_name(self):
        return self._get_name(r'\.ru/([^/]+)')


main = SelfMangaRu
