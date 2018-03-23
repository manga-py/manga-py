from manga_py.provider import Provider
from .helpers.std import Std


class MangaDexCom(Provider, Std):
    _links_on_page = 100
    _home_url = ''

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        ch = self.chapter[0]
        re = self.re.compile(r'[vV]ol.+?(\d+).+?[cC]h.+?(\d+(?:.\d+)?)')
        return '{}-{}'.format(*self._idx_to_x2(re.search(ch).groups()))

    def get_main_content(self):
        url = self.get_url()
        if url.find('/manga/') < 0:
            url = self.html_fromstring(url, '.toggle.col-sm-2 > a', 0)
            url = self.http().normalize_uri(url.get('href'))
        return self.http_get(url)

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/manga/'):
            name = self.html_fromstring(url, 'h3.panel-title', 0)
        else:
            name = self.html_fromstring(url, '.toggle.col-sm-2 > a', 0)
        return name.text_content().strip()

    def get_chapters(self):
        parser = self.document_fromstring(self.content)
        pages = self._get_pages_count(parser)
        items = self._chapters(parser)
        for i in range(pages):
            n = i * self._links_on_page
            parser = self.html_fromstring('%s/%d' % (self._links_on_page, n))
            items += self._chapters(parser)
        return self._parse_chapters(items)

    def get_files(self):
        content = self.http_get(self.chapter[1])
        items = self.re.search(r'page_array.+\n?(.+),]', content)
        data = self.re.search(r'dataurl\s*=\s*[\'"](.+)[\'"]', content)
        server = self.re.search(r'server\s*=\s*[\'"](.+)[\'"]', content)
        if not items or not data or not server:
            return []
        items = items.group(1).strip(' \'').split('\',\'')
        data = data.group(1)
        server = server.group(1)
        domain = self.domain
        return ['{}{}{}/{}'.format(domain, server, data, i) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.edit .col-sm-3 img')

    def prepare_cookies(self):
        self._storage['cookies']['mangadex_h_toggle'] = '1'

    def _parse_chapters(self, items):
        n = self.http().normalize_uri
        return [(i.text_content(), n(i.get('href'))) for i in items]

    @staticmethod
    def _chapters(parser):
        return parser.cssselect('#chapters tr td:first-child a')

    def _get_pages_count(self, parser):
        pages = parser.cssselect('.pagination .paging > a')
        count = 0
        if pages:
            re = self.re.compile(r'.+/(\d+)')
            count = re.search(pages[-1].get('href')).group(1)
        return int(count / self._links_on_page)


main = MangaDexCom
