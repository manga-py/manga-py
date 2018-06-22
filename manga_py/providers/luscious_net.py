from manga_py.provider import Provider
from .helpers.std import Std


class LusciousNet(Provider, Std):

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_main_content(self):
        name = self._get_name('/albums?/([^/]+)/')
        return self.http_get('{}/albums/{}/'.format(self.domain, name))

    def get_manga_name(self) -> str:
        return self._get_name('/albums?/([^/]+)_\d+/')

    def get_chapters(self):
        return [b'0']

    def get_files(self):
        items = self._elements('#album_meta_ds .item > a')
        n = self.http().normalize_uri
        images = []
        for i in items:
            content = self.http_get(n(i.get('href')), headers={'x-requested-with': 'XMLHttpRequest'})
            image = self.document_fromstring(content, '#single_picture')
            if image:
                images.append(n(image[0].get('src')))
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.album_cover_item img')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = LusciousNet
