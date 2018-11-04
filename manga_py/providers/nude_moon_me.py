from manga_py.provider import Provider
from .helpers.std import Std
from manga_py.fs import basename


class NudeMoonMe(Provider, Std):
    __content = None
    __url = None

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_main_content(self):
        return self.__content

    def get_manga_name(self) -> str:
        self.__url = self.get_url()
        if not self.re.search(r'\d+-online--', self.__url):
            _url = self.re.search(r'(.+?/\d+)--(.+\.html)', self.__url)
            self.__url = '{}-online--{}'.format(*_url.groups())
        self.__content = self.http_get(self.__url + '?row')
        name = self.document_fromstring(self.__content, 'meta[property="og:title"]', 0).get('content')
        name = self.re.search(r'(.+?) [#/]', name)
        return name.group(1) if name else basename(self.__url)

    def get_chapters(self):
        return [b'']

    def get_files(self):
        return [i.get('src') for i in self._elements('.square-red center > img')]

    def get_cover(self) -> str:
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.__url


main = NudeMoonMe
