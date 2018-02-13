from src.provider import Provider


class PuzzmosCom(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(
            idx[0],
            0 if len(idx) < 2 else idx[1]
        )

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        idx = self.re.search('/manga/([^/]+)/', chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/manga/([^/]+)', self.get_url())

    def get_chapters(self):
        return self.html_fromstring(self.get_storage_content(), '#bolumler td a')

    @staticmethod
    def _get_image(parser):
        img = parser.cssselect('.chapter-content img.chapter-img')
        if img:
            return [img.get('src')]
        return []

    def get_files(self):
        url = self.get_current_chapter()
        parser = self.html_fromstring(url)
        pages = parser.cssselect('.label-info + select')[0].cssselect('option + option')
        images = self._get_image(parser)
        for i in pages:
            parser = self.html_fromstring(i.get('value'))
            images += self._get_image(parser)
        return images

    def get_cover(self) -> str:
        return self._get_cover_from_content('img.thumbnail.manga-cover')


main = PuzzmosCom
