from manga_py.provider import Provider
from .helpers.std import Std
import requests


class RawDevArtComOld(Provider, Std):
    _chapter_selector = r'/chapter/[^\d]+(\d+(?:\.\d+)?)'

    def get_chapter_index(self) -> str:
        idx = self.re.search(self._chapter_selector, self.chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        items = self._elements('.wp-manga-chapter > a')

        if len(items) == 0:  # example: https://mangasushi.net
            manga_id = self._elements('#manga-chapters-holder')[0].get('data-id')
            items_content = requests.post('{}/wp-admin/admin-ajax.php'.format(self.domain), data={
                'action': 'manga_get_chapters',
                'manga': manga_id,
            }).text
            items = self._elements('.wp-manga-chapter > a', items_content)


        return items

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.page-break img.wp-manga-chapter-img')

    def get_cover(self) -> str:
        return self._cover_from_content('.summary_image img.img-responsive')


main = RawDevArtComOld
