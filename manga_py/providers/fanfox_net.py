from manga_py.provider import Provider
from .helpers.std import Std
from manga_py.crypt.base_lib import BaseLib


class MangaFoxMe(Provider, Std):

    def get_archive_name(self) -> str:
        groups = self._ch_parser()
        ch = groups[1].replace('.', '-')
        vol = ['0']
        if groups[0]:
            vol = [groups[0]]
        return self.normal_arc_name({'vol': vol, 'ch': ch})

    def _ch_parser(self):
        selector = r'/manga/[^/]+/(?:v([^/]+)/)?c([^/]+)/'
        groups = self.re.search(selector, self.chapter).groups()
        return groups

    def get_chapter_index(self) -> str:
        groups = self._ch_parser()
        idx = groups[1].replace('.', '-')
        if not ~idx.find('-'):
            idx = idx + '-0'
        if groups[0]:
            return '{}-{}'.format(idx, groups[0])
        return idx

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)/?')

    def get_chapters(self):
        return self._elements('[id^="list-"] a[href]')

    def _get_links(self, content):
        js = self.re.search(r'eval\((function\b.+)\((\'[\w ].+)\)\)', content).groups()
        return BaseLib.exec_js('m = ' + js[0], 'm(' + js[1] + ')')

    def _one_link_helper(self, content, page):
        cid = self.re.search(r'chapterid\s*=\s*(\d+)', content).group(1)
        base_url = self.chapter[0:self.chapter.rfind('/')]
        links = self._get_links(content)
        key = ''.join(self.re.findall(r'\'(\w)\'', links))
        return self.http_get('{}/chapterfun.ashx?cid={}&page={}&key={}'.format(
            base_url,
            cid,
            page,
            key
        ))

    def _parse_links(self, data):
        base_path = self.re.search(r'pix="(.+?)"', data).group(1)
        images = self.re.findall(r'"(/\w.+?)"', data)
        return [base_path + i for i in images]

    def _get_links_page_to_page(self, content):
        last_page = self.document_fromstring(content, '.pager-list-left > span > a:nth-last-child(2)', 0)
        links = []
        for i in range(0, int(int(last_page.get('data-page'))/2 + .5)):
            data = self._one_link_helper(content, (i*2)+1)
            links += self._parse_links(self._get_links(data))
        return links

    def get_files(self):
        content = self.http_get(self.chapter)
        links = self._get_links(content)

        n = self.http().normalize_uri

        if ~links.find('key='):
            # chapters data example: http://fanfox.net/manga/the_hero_is_overpowered_but_overly_cautious/c001/chapterfun.ashx?cid=567602&page=6&key=6b5367d728d445a8
            return self._get_links_page_to_page(content)

        if ~links.find('token='):
            links_array = self.re.search(r'(\[.+?\])', links)
            links_array = links_array.group(1).replace('\'', '"')
            links_data = self.json.loads(links_array)
            return [n(i) for i in links_data]

        data = self.re.search(r'\w=(\[.+\])', links).group(1)
        data = self.json.loads(data.replace("'", '"'))
        return [n(i) for i in data]

    def get_cover(self):
        return self._cover_from_content('img.detail-info-cover-img')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def prepare_cookies(self):
        self.http().cookies['isAdult'] = '1'


main = MangaFoxMe
