from manga_py.provider import Provider
from .helpers.std import Std


class TruyenTranhTuanCom(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'\.\w{2,7}/[^/]+?-(\d+(?:-\d+)?)', self.chapter)
        return idx.group(1)

    def get_content(self):
        content = self.http_get(self.get_url())
        parser = self.document_fromstring(content, '#read-title a.mangaName')
        if parser and len(parser):
            return self.http_get(self.http().normalize_uri(parser[0].get('href')))
        return content

    def get_manga_name(self) -> str:
        url = self.get_url()
        if self.re.search(r'\.\w{2,7}/[^/]+-\d+/', url):
            parser = self.html_fromstring(url, '#read-title .mangaName', 0)
            url = parser.get('href')
        return self.re.search(r'\.\w{2,7}/([^/]+)/', url).group(1)

    def get_chapters(self):
        return self._elements('#manga-chapter .chapter-name a')

    def get_files(self):
        content = self.http_get(self.chapter)
        items = self.re.search(r'slides_page_url_path\s*=\s*(\[.+\])[;,]?', content)
        if items:
            n = self.http().normalize_uri
            items = self.json.loads(items.group(1))
            return [n(i) for i in items]
        return []

    def get_cover(self) -> str:
        return self._cover_from_content('.manga-cover img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = TruyenTranhTuanCom
