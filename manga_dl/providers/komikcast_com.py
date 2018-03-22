from manga_dl.provider import Provider
from .helpers.std import Std


class KomikCastCom(Provider, Std):
    _chapter_re = r'\.com/[^/]+-(\d+(?:-\d+)?)'

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/chapter/'):
            url = self.html_fromstring(url, '.allc a', 0).get('href')
            self._params['url'] = self.http().normalize_uri(url)
            return self.get_manga_name()
        return self._get_name(r'\.com/([^/]+)')


main = KomikCastCom
