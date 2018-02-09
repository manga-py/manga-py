from src.provider import Provider


class SoMangaNet(Provider):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return self.re.search('/leitor/[^/]+/([^/]+)').group(1)

    def get_main_content(self):
        return self.http_get('{}/manga/{}'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        return self.re.search(r'\.net/[^/]+/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        return self.document_fromstring(self.get_storage_content(), 'ul.capitulos li > a')

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter(), 'img.img-manga')
        return [i.get('src') for i in parser]


main = SoMangaNet
