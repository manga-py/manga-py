from manga_py.provider import Provider
from .helpers.std import Std


class MangaTailCom(Provider, Std):
    __local_storage = None

    def get_archive_name(self) -> str:
        return self.normal_arc_name([
            self.chapter_id,
            *self._parse_ch(self.chapter[0]).split('.')
        ])

    def get_chapter_index(self) -> str:  # Oh ...
        pass

    def _parse_ch(self, chapter):
        _re = r'.+?[^\d](\d+(?:\.\d+)?)'
        if ~chapter.find('-fixed'):
            _re = r'.+?[^\d](\d+(?:\.\d+)?).+fixed'
        re = self.re.search(_re, chapter, self.re.I)
        if re:
            return re.group(1)
        return chapter

    def get_main_content(self):
        url = self.get_url()
        if self.__local_storage:
            url = self.__local_storage
        return self.http_get(url)

    def get_manga_name(self) -> str:
        selector = '.main-content-inner .page-header'
        header = self.html_fromstring(self.get_url(), selector, 0)
        link = header.cssselect('a.active + a')
        if link:
            link = self.http().normalize_uri(link.get('href'))
            self.__local_storage = link
            header = self.html_fromstring(link, selector, 0)
        return header.text_content().strip().replace('/', '_')  # http://www.mangasail.com/content/12-prince-manga

    def _fix_chapters(self, items):
        # http://www.mangasail.com/content/go-toubun-no-hanayome-30-%E2%80%93-fixed
        # I wanted to sleep. Maybe fix it someday.
        found = []
        result = []
        n = self.http().normalize_uri
        for i in items:
            name, url = i.text_content().strip(), i.get('href')
            _name = self._parse_ch(name)
            if ~url.find('-fixed'):
                found.append(_name)
        for i in items:
            name = i.text_content().strip()
            _name = self._parse_ch(name)
            url = i.get('href')
            if _name not in found or ~url.find('-fixed'):
                result.append((name, n(url)))
        return result

    def get_chapters(self):
        items = self.document_fromstring(self.content, '.chlist td a')
        items = self._fix_chapters(items)
        return sorted(items, key=lambda n: float(self._parse_ch(n[0])), reverse=True)

    def prepare_cookies(self):
        self._base_cookies()

    def get_files(self):
        url = self.chapter[1]
        items = self.html_fromstring('{}{}'.format(url, '?page=all'), '#images img')
        n = self.http().normalize_uri
        return [n(i.get('src')) for i in items]

    def get_cover(self) -> str:  # TODO
        cover = self.document_fromstring(self.content, 'iframe.authcache-esi-assembly', 0)
        cover = self.json.loads(cover.text_content().strip()).get('field')
        key = cover.keys()[0]
        cover = self.document_fromstring(cover.get(key), '.field-type-image img', 0)
        return self.http().normalize_uri(cover.get('src'))

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.chapter[1]


main = MangaTailCom
