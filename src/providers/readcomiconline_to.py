from src.provider import Provider


class ReadComicOnlineTo(Provider):
    __local_storage = None

    def get_archive_name(self) -> str:
        chapter = self.re.search('id=(\d+)', self.get_current_chapter()).group(1)
        idx = self.get_chapter_index(True).split('-')[0]
        return 'vol_{:0>3}-{}'.format(idx, chapter)

    def get_chapter_index(self, no_increment=False) -> str:
        if not no_increment:
            self.__local_storage += 1
        return '{}-0'.format(self.__local_storage)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/Comic/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('\\.to/Comic/([^/]+)', self.get_url())

    def get_chapters(self):
        items = self.document_fromstring(self.get_storage_content(), 'table.listing td > a')
        domain = self.get_domain()
        return ['{}/{}&readType=1'.format(domain, i.get('href')) for i in items]

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        items = self.re.findall('lstImages.push\("([^"]+)"\)', content)
        return items

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = ReadComicOnlineTo
