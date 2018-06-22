from manga_py.provider import Provider
from .helpers.std import Std


class HentaiFoxCom(Provider, Std):
    __local_storage = None
    _idx_re = r'/g(?:allery)?/(\d+)'
    _url_str = '{}/gallery/{}/'
    _name_selector = '.info h1'

    def get_archive_name(self) -> str:
        return self.get_chapter_index()

    def get_chapter_index(self) -> str:
        return 'archive'

    def get_main_content(self):
        if self.__local_storage is None:
            idx = self._get_name(self._idx_re)
            url = self._url_str.format(self.domain, idx)
            self.__local_storage = self.http_get(url)
        return self.__local_storage

    def get_manga_name(self) -> str:
        return self.text_content(self.content, self._name_selector)

    def get_chapters(self):
        return [b'']

    def get_files(self):
        pages = self._elements('.gallery .preview_thumb a')
        items = []
        n = self.http().normalize_uri
        for i in pages:
            url = self.html_fromstring(n(i.get('href')), '#gimg', 0).get('src')
            items.append(n(url))
        return items

    def get_cover(self) -> str:
        return self._cover_from_content('.cover img')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = HentaiFoxCom
