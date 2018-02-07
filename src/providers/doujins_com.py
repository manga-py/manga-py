from src.provider import Provider


class DoujinsCom(Provider):

    def get_archive_name(self) -> str:
        name = self.re.search('/gallery/([^/]+)', self.get_url())
        return name.group(1)

    def get_chapter_index(self) -> str:
        return '0'

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        # todo: folders downloading m.b. ?
        return self.__class__.__name__

    def get_chapters(self):
        return [self.get_url()]

    def get_files(self):
        selector = '#image-container img.doujin'
        items = self.html_fromstring(self.get_current_chapter(), selector)
        return [i.get('data-file').replace('&amp;', '&') for i in items]

    def get_cover(self) -> str:
        pass


main = DoujinsCom
