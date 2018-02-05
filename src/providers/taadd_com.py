from src.provider import Provider


class TaaddCom(Provider):
    __local_storage = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-', 2)
        return self.remove_not_ascii('vol_{:0>3}-{}'.format(*idx))

    def get_chapter_index(self, no_increment=False) -> str:
        if not no_increment:
            self.__local_storage += 1
        idx = self.re.search('/chapter/([^/]+)/', self.get_current_chapter()).group(1)
        return '{}-{}'.format(self.__local_storage, idx)

    def get_main_content(self):
        name = self._storage.get('manga_name', self.get_manga_name())
        return '{}/book/{}.html'.format(self.get_domain(), name)

    def _re_name(self, url):
        return self.re.search('/book/([^/]+)\\.html', url)

    def get_manga_name(self) -> str:
        url = self.get_url()
        name = self._re_name(url)
        if not name:
            selector = 'h1.chapter_bar .postion .normal a[href*="/book/"]'
            name = self.html_fromstring(url, selector, 0).get('href')
            name = self._re_name(name)
        return name.group(1)

    def get_chapters(self):
        items = self.document_fromstring(self.get_storage_content(), '.chapter_list td[align="left"] a')
        return [self.http().normalize_uri(i.get('href')) for i in items]

    def prepare_cookies(self):
        self.__local_storage = 0

    @staticmethod
    def __get_image(parser):
        return parser.cssselect('#comicpic')[0].get('src')

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        pages = parser.cssselect('#page')[0].cssselect('option + option')
        images = [self.__get_image(parser)]
        for i in pages:
            c = self.html_fromstring(self.http().normalize_uri(i.get('value')))
            images.append(self.__get_image(c))
        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = TaaddCom
