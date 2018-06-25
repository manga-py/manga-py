from manga_py.provider import Provider
from .helpers.std import Std


class TaaddCom(Provider, Std):
    __local_storage = None
    _name_selector = 'h1.chapter_bar a[href*="/book/"]'
    _pages_selector = '#page'
    _chapters_selector = '.chapter_list td[align="left"] a'
    img_selector = '#comicpic'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return self.remove_not_ascii(self.normal_arc_name([
            self.chapter_id, idx
        ]))

    def get_chapter_index(self) -> str:
        idx = self.re.search('/chapter/([^/]+)/', self.chapter).group(1)
        return idx

    def get_main_content(self):
        return self.http_get('{}/book/{}.html'.format(self.domain, self.manga_name))

    def _re_name(self, url):
        return self.re.search(r'/book/([^/]+)\.html', url)

    def get_manga_name(self) -> str:
        url = self.get_url()
        name = self._re_name(url)
        if not name:
            name = self.html_fromstring(url, self._name_selector, 0).get('href')
            name = self._re_name(name)
        return name.group(1)

    def get_chapters(self):
        return self._elements(self._chapters_selector)

    def prepare_cookies(self):
        self.__local_storage = 0

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        pages = parser.cssselect(self._pages_selector)[0].cssselect('option + option')
        images = self._images_helper(parser, self.img_selector)
        for i in pages:
            c = self.html_fromstring(self.http().normalize_uri(i.get('value')))
            images += self._images_helper(parser, self.img_selector)
        return images

    def book_meta(self) -> dict:
        # todo meta
        pass


main = TaaddCom
