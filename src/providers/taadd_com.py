from src.provider import Provider


class TaaddCom(Provider):
    __local_storage = None
    _name_selector = 'h1.chapter_bar a[href*="/book/"]'
    _pages_selector = '#page'
    _chapters_selector = '.chapter_list td[align="left"] a'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        name = 'vol_{:0>3}-{}'.format(self._chapter_index(), idx)
        return self.remove_not_ascii(name)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/chapter/([^/]+)/', self.get_current_chapter()).group(1)
        return idx

    def get_main_content(self):
        name = self._storage.get('manga_name', self.get_manga_name())
        return self.http_get('{}/book/{}.html'.format(self.get_domain(), name))

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
        return self.document_fromstring(self.get_storage_content(), self._chapters_selector)

    def prepare_cookies(self):
        self.__local_storage = 0

    @staticmethod
    def _get_image(parser):
        return [parser.cssselect('#comicpic')[0].get('src')]

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        pages = parser.cssselect(self._pages_selector)[0].cssselect('option + option')
        images = self._get_image(parser)
        for i in pages:
            c = self.html_fromstring(self.http().normalize_uri(i.get('value')))
            images += self._get_image(parser)
        return images


main = TaaddCom
