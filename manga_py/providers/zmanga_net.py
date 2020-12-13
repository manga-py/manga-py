from manga_py.provider import Provider
from .helpers.std import Std


class ZMangaNet(Provider, Std):
    _type = 'capitulo'

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'%s-(\d+(?:-\d+)?)' % self._type)
        return re.search(self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/manga-online/{}/')

    def get_manga_name(self) -> str:
        re = r'\.\w{2,7}(?:/manga-online|/read)?/([^/]+?)(?:-%s[^/]+)?/' % self._type
        return self._get_name(re)

    def get_chapters(self):
        return self._elements('.mangabox_line > a')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        items = self._images_helper(parser, 'meta[property="og:image:secure_url"]', 'content')
        if len(items) < 1:
            items = self._images_helper(parser, 'meta[property="og:image"]', 'content')
        return items

    def get_cover(self) -> str:
        # return self._cover_from_content('.cover img')
        pass

    def book_meta(self) -> dict:
        pass


main = ZMangaNet
