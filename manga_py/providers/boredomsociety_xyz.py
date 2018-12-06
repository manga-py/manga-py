from manga_py.provider import Provider
from .helpers.std import Std


class BoredomSocietyXyz(Provider, Std):
    def get_chapter_index(self) -> str:
        return self.re.search(
            r'/reader/\d+/(\d+(?:\.\d+)?)',
            self.chapter
        ).group(1).replace('.', '-')

    def get_main_content(self):
        idx = self.re.search(
            '/(?:titles/info|reader)/(\d+)',
            self.get_url()
        ).group(1)
        return self.http_get('{}/titles/info/{}'.format(
            self.domain,
            idx
        ))

    def get_manga_name(self) -> str:
        return self.text_content(self.content, 'h2')

    def get_chapters(self):
        return self._elements('a.titlesinfo_chaptertitle')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        images = self._images_helper(parser, 'img.reader_mangaimage')
        n = self.http().normalize_uri
        return [n(i) for i in images]

    def get_cover(self) -> str:
        return self._cover_from_content('img.titlesinfo_coverimage')

    def book_meta(self) -> dict:
        pass

    def prepare_cookies(self):
        # enable "all-images-on-page"
        self.http_post('{}/module/reader/ajax.php'.format(self.domain), data={
            'readingtype': 'all'
        })


main = BoredomSocietyXyz
