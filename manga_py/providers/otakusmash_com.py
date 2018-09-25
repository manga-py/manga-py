from manga_py.provider import Provider
from .helpers.std import Std


class OtakuSmashCom(Provider, Std):
    selector = r'https?://[^/]+/(read-\w+/|reader/)?([^/]+)'
    prefix = '/'

    def get_chapter_index(self) -> str:
        selector = self.selector + '/([^/]+)'
        idx = self.re.search(selector, self.chapter)
        return '-'.join(*idx.group(3).split('.'))

    def get_main_content(self):
        return self.http_get(self._get_manga_url())

    def get_manga_name(self) -> str:
        result = self.re.search(self.selector, self.get_url())
        self.prefix = result.group(1)
        return result.group(2)

    def get_chapters(self):
        parser = self.document_fromstring(self.content)
        items = self._first_select_options(parser, '.pager select[name="chapter"]', False)
        url = self._get_manga_url()
        return ['{}{}/'.format(url, i.get('value')) for i in items]

    def get_files(self):
        chapter = self.chapter
        parser = self.html_fromstring(chapter)
        pages = self._first_select_options(parser, '.mid .pager select[name="page"]')
        images = []
        _img = self._get_image(parser)
        _img and images.append(_img)
        for page in pages:
            parser = self.html_fromstring('{}{}/'.format(chapter, page.get('value')))
            _img = self._get_image(parser)
            _img and images.append(_img)
        return images

    def _get_manga_url(self):
        return '{}/{}{}/'.format(self.domain, self.prefix, self.manga_name)

    def _get_image(self, parser):
        image = parser.cssselect('a > img.picture')
        if not len(image):
            return False
        image = image[0].get('src')
        if image[0] == '/':
            return self.http().normalize_uri(image)
        base_uri = parser.cssselect('base')
        if len(base_uri):
            base_uri = base_uri[0].get('href')
        else:
            base_uri = self.chapter
        return base_uri + image

    def get_cover(self):
        pass  # TODO

    def book_meta(self) -> dict:
        # todo meta
        pass


main = OtakuSmashCom
