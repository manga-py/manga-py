from urllib.parse import unquote_plus

from manga_py.provider import Provider
from .helpers.std import Std


class MangaCanBlogCom(Provider, Std):
    _home_link = None

    def get_archive_name(self) -> str:
        ch = self.chapter
        idx = self.re.search(r'/.+/.+?(?:-indonesia-)(.+)\.html', ch)
        if not idx:
            idx = self.re.search(r'/.+/(.+)\.html', ch)
        idx = idx.group(1)
        if ~idx.find('-terbaru'):
            idx = idx[:idx.find('-terbaru')]
        return self.normal_arc_name({'vol': [self.chapter_id, idx]})

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        return self.http_get(self._home_link)

    @staticmethod
    def _clear_name(a):
        name = a.text_content()
        name = unquote_plus(name.split('|')[0].strip())
        if ~name.find(' Indonesia'):
            name = name[:name.find(' Indonesia')]
        return name

    def get_manga_name(self) -> str:
        url = self.get_url()
        selector = '.navbar a[href*=".html"]'
        content = self.http_get(url)
        a = self.document_fromstring(content)
        is_chapter = a.cssselect(selector)
        if len(is_chapter) < 1:
            selector = '#latestchapters h1'
            a = a.cssselect(selector)
            self._home_link = url
        else:
            a = is_chapter[0]
            self._home_link = a.get('href')
        return self._clear_name(a)

    def get_chapters(self):
        items = self._elements('a.chaptersrec')
        result = []
        for i in items:
            url = i.get('href')
            _ = url.find('-terbaru-1')
            if _:
                url = url[:_] + '-terbaru.html'
            result.append(url)
        return result

    def get_files(self):
        content = self.http_get(self.chapter)
        items = self._elements('#imgholder .picture', content)
        return [i.get('src') for i in items]

    def get_cover(self) -> str:
        # return self._cover_from_content('.cover img')
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaCanBlogCom
