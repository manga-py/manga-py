from .rawdevart_com_old import RawDevArtComOld


class ManhwaClub(RawDevArtComOld):
    _chapter_selector = r'/chapter-(\d+(?:\.\d+)?)'

    def get_content(self):
        return self._get_content('{}/manhwa/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manhwa/([^/]+)')


main = ManhwaClub
