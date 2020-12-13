from manga_py.provider import Provider
from .helpers.std import Std


class HentaiHereCom(Provider, Std):
    _cdn = 'https://hentaicdn.com/hentai'

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        idx = self.re.search('/m/[^/]+/([^/]+(?:/[^/]+))', chapter)
        return idx.group(1).replace('/', '-')

    def get_content(self):
        url = self.re.search('(/m/[^/]+)', self.get_url())
        url = '{}{}'.format(self.domain, url.group(1))
        return self.http_get(url)

    def get_manga_name(self) -> str:
        selector = 'span.hide[itemscope] span[itemprop="name"]'
        name = self.document_fromstring(self.content, selector)
        if not name:
            selector = '#detail span[itemprop="title"]'
            name = self.document_fromstring(self.content, selector)
        return name[0].text_content().strip()

    def get_chapters(self):
        return self._elements('ul.arf-list > li > a')

    def get_files(self):
        chapter = self.chapter
        content = self.http_get(chapter)
        items = self.re.search(r'_imageList\s*=\s*(\[".+"\])', content).group(1)
        return [self._cdn + i for i in self.json.loads(items)]

    def get_cover(self) -> str:
        return self._cover_from_content('#cover img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = HentaiHereCom
