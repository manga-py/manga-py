from manga_py.provider import Provider
from .helpers.std import Std


class LeoMangaCom(Provider, Std):

    def get_chapter_index(self) -> str:
        url = self.chapter
        idx = self.re.search(r'/manga/[^/]+/capitulo-(\d+)/([^/]+)/', url).groups()
        return '{1}-{0}'.format(*idx)

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def _get_first_href(self, parser):
        n = self.http().normalize_uri
        url = n(parser[0].get('href'))
        select0 = self.html_fromstring(url, '.list-group .cap-option')
        if select0:
            return n(select0[0].get('href'))
        return None

    def get_chapters(self):
        chapter = self.document_fromstring(self.content, '.caps-list a')
        if chapter:
            url = self._get_first_href(chapter)
            if url:
                selector = '.viewcap-info select.form-control'
                parser = self.html_fromstring(url)
                options = self._first_select_options(parser, selector)
                return [i.get('value') for i in options[::-1]]
        return []

    def get_files(self):
        n = self.http().normalize_uri
        items = self.html_fromstring(self.chapter, '.vertical .cap-images')
        return [n(i.get('src')) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.cover img', 'data-original')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = LeoMangaCom
