from src.provider import Provider


class MangaAe(Provider):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return self.re.search(r'\.ae/[^/]+/(\d+)', self.get_current_chapter()).group(1)

    def get_main_content(self):
        return self.http_get('{}/{}/'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        return self.re.search(r'\.ae/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        selector = 'li > a.chapter'
        items = self.document_fromstring(self.get_storage_content(), selector)
        return [i.get('href') for i in items]

    @staticmethod
    def _get_image(parser):
        img = parser.cssselect('#showchaptercontainer img')
        return img[0].get('src') if img else None

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter())
        pages = parser.cssselect('#morepages a + a')
        _ = self._get_image(parser)
        images = []
        _ and images.append(_)
        if pages:
            for i in pages:
                parser = self.html_fromstring(i.get('href'))
                _ = self._get_image(parser)
                _ and images.append(_)
        return images

    def get_cover(self) -> str:
        return self._get_cover_from_content('img.manga-cover')


main = MangaAe
