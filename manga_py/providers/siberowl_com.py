from manga_py.provider import Provider
from .helpers.std import Std


class SiberOwlCom(Provider, Std):
    _main_fmt = '{}/mangas/{}/'
    n = None

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/mangas/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1).replace('.', '-')

    def get_main_content(self):
        return self._get_content(self._main_fmt)

    def get_manga_name(self) -> str:
        return self._get_name(r'/mangas/([^/]+)')

    def get_chapters(self):
        re = self.re.compile(r'chapString\s*=\s*"(.+)";')
        elements = self.document_fromstring(
            re.search(self.content).group(1),
            'a'
        )
        return ['{}/mangas/{}/{}'.format(
            self.domain,
            self.manga_name,
            i.get('href')
        ) for i in elements]

    def get_files(self):
        content = self.http_get(self.chapter)
        re = self.re.search(r'imageUrls\s*=\s*(\[.*\])', content)
        items = re.group(1)
        if not items:
            return []
        items = self.json.loads(self.re.sub(r'(.+)",\]', r'\1"]', items))
        return ['{}{}'.format(self.domain, i) for i in items]

    def get_cover(self) -> str:
        re = self.re.compile(r'imageUrl\s*=\s*"(.+)";')
        return '{}{}'.format(
            self.domain,
            re.search(self.content).group(1)
        )

    def book_meta(self) -> dict:
        # todo meta
        pass


main = SiberOwlCom
