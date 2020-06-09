from .rawdevart_com import RawDevArtCom


class ManhwaClub(RawDevArtCom):
    _chapter_selector = r'/chapter-(\d+(?:\.\d+)?)'

    def get_main_content(self):
        return self._get_content('{}/manhwa/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manhwa/([^/]+)')


main = ManhwaClub
