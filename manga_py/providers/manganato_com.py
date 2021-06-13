from .manganelo_com import MangaNeloCom


class MangaNatoCom(MangaNeloCom):
    _prefix = '/manga-'
    __alternative_cdn = 'https://bu2.mkklcdnv6tempv2.com'

    def get_manga_name(self) -> str:
        return self._get_name('/manga-([^/]+)')

    def prepare_cookies(self):
        self.http().allow_send_referer = True
        self.http().referer = self.domain


main = MangaNatoCom
