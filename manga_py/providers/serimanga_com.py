from manga_py.provider import Provider
from .helpers.std import Std


class SeriMangaCom(Provider, Std):
    def get_chapter_index(self) -> str:
        idx = self.chapter[1].split('.')
        return '-'.join([
            idx[0],
            idx[1] if len(idx) > 1 else '0',
        ])

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga/([-\w]+)')

    def get_chapters(self):
        items = self._elements('li.spl-list-item a')
        n = self.http().normalize_uri
        return [(n(i.get('href')), i.cssselect('span')[0].text_content().strip()) for i in items]

    def get_files(self):
        parser = self.html_fromstring(self.chapter[0])
        images = self._images_helper(parser, '.chapter-pages > img', 'data-src', 'src')
        n = self.http().normalize_uri
        return [n(image) for image in images]

    def get_cover(self) -> str:
        return self.parse_background(self._elements('.seri-img')[0])

    def chapter_for_json(self) -> str:
        return self.chapter[0]


main = SeriMangaCom
