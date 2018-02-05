from src.provider import Provider


class MyReadingMangaInfo(Provider):
    __local_storage = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self, no_increment=False) -> str:
        if not no_increment:
            self.__local_storage += 1
        return '{}-0'.format(self.__local_storage)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/{}/'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('\\.info/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        url = self.get_url()
        content = self.get_storage_content()
        v = [url]  # current chapter
        parser = self.document_fromstring(content, '.entry-content p > a')
        v += [i.get('href') for i in parser]
        return v[::-1]

    def prepare_cookies(self):
        self.__local_storage = 0
        self.cf_protect(self.get_url())

    def get_files(self):
        selector = '.entry-content div img,.entry-content p img'
        parser = self.html_fromstring(self.get_current_chapter(), selector)
        return [i.get('src') for i in parser]

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MyReadingMangaInfo
