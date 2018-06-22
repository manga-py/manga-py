from manga_py.provider import Provider
from .helpers.std import Std


class FreeAdultComixCom(Provider, Std):

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        return [b'']

    def _external_images(self):  # https://freeadultcomix.com/star-vs-the-forces-of-sex-iii-croc/
        links = self._elements('.single-post p > a[target="_blank"] > img')
        items = []
        re = self.re.compile(r'(.+/)th(/.+)')
        for i in links:
            g = re.search(i.get('src')).groups()
            items.append('{}/i/{}/0.jpg'.format(*g))
        return items

    def get_files(self):
        images = self._elements('.single-post p > img[class*="wp-image-"]')
        if not len(images):
            items = self._external_images()
        else:
            items = [i.get('src') for i in images]
        return items

    def get_cover(self) -> str:
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = FreeAdultComixCom
