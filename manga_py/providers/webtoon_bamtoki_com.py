from manga_py.crypt.base_lib import BaseLib
from manga_py.provider import Provider
from .helpers.std import Std


class WebtoonBamtokiCom(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'.+-(\d+).html')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        url = self.get_url()
        _selector = r'\.(?:com|se)/(.+)'
        if ~url.find('.html'):
            _selector += r'-\d+\.html'
        return self._get_name(_selector)

    def get_chapters(self):
        return self._elements('.list-details a.ellipsis')

    def get_files(self):
        data = self.html_fromstring(self.chapter, '#tooncontentdata', 0)
        content = BaseLib.base64decode(data.text_content().strip('\n\t\r\0 '))
        parser = self.document_fromstring(content)
        return self._images_helper(parser, 'img')

    def get_cover(self) -> str:
        return self._cover_from_content('.title-section-inner .col-md-6 > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = WebtoonBamtokiCom
