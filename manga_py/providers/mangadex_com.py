from manga_py.provider import Provider
from .helpers.std import Std


class MangaDexCom(Provider, Std):
    _links_on_page = 100
    _home_url = ''

    def get_archive_name(self) -> str:
        return self.normal_arc_name({
            'vol': self.chapter['vol'],
            'ch': [*self.chapter['ch'].split('.'), self.chapter['lng']],
        })

    def get_chapter_index(self) -> str:
        fmt = '{}-{}'
        if len(self.chapter['lng']) > 0:
            fmt += '-{}'
        return fmt.format(
            self.chapter['ch'].replace('.', '-'),
            self.chapter['vol'],
            self.chapter['lng'],
        )

    def get_main_content(self):
        url = self.get_url()
        if url.find('/title/') < 0:
            url = self.html_fromstring(url, 'a.manga-link', 0)
            url = self.http().normalize_uri(url.get('href'))
        self._home_url = self.re.search('(.+/title/\d+/[^/])', url).group(1)
        return self.http_get(self._home_url)

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/title/'):
            name = self.html_fromstring(url, '.card-header', 0).text_content()
        else:
            name = self.html_fromstring(url, '.manga-link', 0).get('title')
        return name.strip()

    def get_chapters(self):
        parser = self.document_fromstring(self.content)
        # https://mangadex.org/manga/153/detective-conan
        pages = parser.cssselect('.pagination li.paging a')
        items = self._get_chapters_links(parser)
        if pages:
            pages = self.re.search(r'.+/(\d+)', pages[0].get('href')).group(1)
            for i in range(2, int(pages)+1):
                _parser = self.html_fromstring('{}/chapters/{}/)'.format(
                    self._home_url, i
                ))
                items += self._get_chapters_links(_parser)
        return self._parse_chapters(items)

    def _get_chapters_links(self, parser):
        return parser.cssselect('div.chapter-row[data-chapter]')

    def get_files(self):
        idx = self.re.search(r'/chapter/(\d+)', self.chapter['link']).group(1)
        try:
            data = self.json.loads(self.http_get('{}/api/chapter/{}'.format(
                self.domain, idx
            )))
            n = self.http().normalize_uri
            items = []
            for item in data.get('page_array', []):
                items.append('{}{}/{}'.format(
                    n(data.get('server', '/data/')), data.get('hash'), item
                ))
            return items
        except Exception as e:
            return []

    def get_cover(self) -> str:
        return self._cover_from_content('.card-body .rounded')

    def prepare_cookies(self):
        self._storage['cookies']['mangadex_h_toggle'] = '1'

    def _parse_chapters(self, items):
        n = self.http().normalize_uri
        result = []
        for tr in items:
            ch = tr.cssselect('a[href*="/chapter/"]')[0]
            lng = tr.cssselect('img.flag')
            result.append({
                'ch': tr.get('data-chapter'),
                'vol': tr.get('data-volume'),
                'link': n(ch.get('href')),
                'lng': lng[0].get('alt') if lng else '',
            })
        return result

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.chapter['link']


main = MangaDexCom
