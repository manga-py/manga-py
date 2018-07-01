from manga_py.provider import Provider
from .helpers.std import Std
from sys import stderr


class MangaDexCom(Provider, Std):
    _links_on_page = 100
    _home_url = ''

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        return self.chapter[0].replace('.', '-')

    def get_main_content(self):
        url = self.get_url()
        if url.find('/manga/') < 0:
            url = self.html_fromstring(url, '.toggle.col-sm-2 > a', 0)
            url = self.http().normalize_uri(url.get('href'))
        self._home_url = self.re.search('(.+/manga/\d+/[^/])', url).group(1)
        return self.http_get(self._home_url)

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/manga/'):
            name = self.html_fromstring(url, 'h3.panel-title', 0)
        else:
            name = self.html_fromstring(url, '.toggle.col-sm-2 > a', 0)
        return name.text_content().strip()

    def get_chapters(self):
        parser = self.document_fromstring(self.content)
        # https://mangadex.org/manga/153/detective-conan
        pages = parser.cssselect('.pagination li.paging:last-of-type a')
        items = self._get_chapters_links(parser)
        if pages:
            pages = self.re.search('.+/(\d+)/', pages[0].get('href')).group(1)
            for i in range(2, int(pages)+1):
                _parser = self.html_fromstring('{}/chapters/{}/)'.format(
                    self._home_url, i
                ))
                items += self._get_chapters_links(_parser)
        return self._parse_chapters(items)

    def _get_chapters_links(self, parser):
        return parser.cssselect('.table [id^=chapter] a[href*="/chapter/"]')

    def get_files(self):
        content = self.http_get(self.chapter[1])
        try:
            files = self.json.loads(self.text_content(content, 'script[data-type="chapter"]'))
            n = self.http().normalize_uri
            server = n(files.get('server'))
            dataurl = files.get('dataurl')
            return ['{}/{}/{}'.format(server, dataurl, file) for file in files.get('page_array')]
        except Exception:
            self.log('Files not found for chapter %s!' % self.chapter[0], file=stderr)
            return []

    def get_cover(self) -> str:
        return self._cover_from_content('.edit .col-sm-3 img')

    def prepare_cookies(self):
        self._storage['cookies']['mangadex_h_toggle'] = '1'

    def _parse_chapters(self, items):
        n = self.http().normalize_uri
        return [(i.get('data-chapter-num'), n(i.get('href'))) for i in items]

    @staticmethod
    def _chapters(parser):
        return parser.cssselect('#chapters tr td:first-child a')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.chapter[1]


main = MangaDexCom
