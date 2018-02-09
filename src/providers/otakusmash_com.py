from src.provider import Provider


class OtakuSmashCom(Provider):
    selector = r'https?://[^/]+/(read\-\w+/|reader/)?([^/]+)'
    prefix = '/'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = self.selector + '/([^/]+)'
        idx = self.re.search(selector, self.get_current_chapter()).group(3).split('.')
        return '{}-{}'.format(
            idx[0],
            0 if len(idx) < 2 else idx[1]
        )

    def get_main_content(self):
        return self.http_get(self._get_manga_url())

    def get_manga_name(self) -> str:
        result = self.re.search(self.selector, self.get_url())
        self.prefix = result.group(1)
        return result.group(2)

    def get_chapters(self):
        content = self.get_storage_content()
        result = self.document_fromstring(content, '.pager select[name="chapter"]', 0)
        items = result.cssselect('option')
        url = self._get_manga_url()
        return ['{}{}/'.format(url, i.get('value')) for i in items]

    def get_files(self):
        chapter = self.get_current_chapter()
        parser = self.html_fromstring(chapter)
        pages = parser.cssselect('.mid .pager select[name="page"]')[0].cssselect('option + option')
        images = []
        _img = self._get_image(parser)
        _img and images.append(_img)
        for page in pages:
            parser = self.html_fromstring('{}{}/'.format(chapter, page.get('value')))
            _img = self._get_image(parser)
            _img and images.append(_img)
        return images

    def _get_manga_url(self):
        name = self.get_manga_name()
        return '{}/{}{}/'.format(self.get_domain(), self.prefix, name)

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
            base_uri = self.get_current_chapter()
        return base_uri + image


main = OtakuSmashCom
