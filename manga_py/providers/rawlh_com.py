from manga_py.provider import Provider
from .helpers.std import Std


class RawLHCom(Provider, Std):
    _root_uri = None

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'-chapter-(.+)\.html')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        content = self._storage.get('main_content', None)
        if content is not None:
            return content
        return self.http_get(self._root_uri)

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/read-'):
            title = self.html_fromstring(url, '.navbar-brand.manga-name', 0)
            self._root_uri = self.http().normalize_uri(title.get('href'))
        else:
            self._root_uri = url
            title = self.document_fromstring(self.content, '.manga-info h1', 0)
        return title.text_content().strip(' \t\r\n\0')

    def get_chapters(self):
        return self._elements('#tab-chapper a.chapter')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.chapter-content img.chapter-img')

    def get_cover(self) -> str:
        return self._cover_from_content('.info-cover img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = RawLHCom
