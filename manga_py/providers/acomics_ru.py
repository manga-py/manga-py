from manga_py.provider import Provider
from .helpers.std import Std


class AComicsRu(Provider, Std):

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_content(self):
        return self._get_content('{}/~{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/~([^/]+)')

    def get_chapters(self):
        return ['~' + self.manga_name]

    def get_files(self):
        pages_max = self.text_content(self.content, 'span.issueNumber').split('/')[1]
        _min = self._params['skip_volumes']
        _max = self._params['max_volumes']
        if _max > 0 and _min > 0:
            _max += _min - 1

        if _max == 0:
            _max = int(pages_max)

        images = []
        for i in range(_min, _max):
            parser = self.document_fromstring(self._get_content('{}/~{}/%d' % (i + 1)))
            images += self._images_helper(parser, '#mainImage')

        return images

    def get_cover(self) -> str:
        return self._cover_from_content('header.serial a img')

    def book_meta(self) -> dict:
        pass

    def prepare_cookies(self):
        self.update_cookies({'ageRestrict': '21'})


main = AComicsRu
