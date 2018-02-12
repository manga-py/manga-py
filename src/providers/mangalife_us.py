from src.provider import Provider


class MangaLifeUs(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>2}-{:0>3}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = r'\-chapter\-(\d+).+(?:\-index\-(\d+))?'
        chapter = self.re.search(selector, self.get_current_chapter()).groups()
        return '{}-{}'.format(
            1 if chapter[1] is None else chapter[1],  # todo: maybe 0 ?
            chapter[0]
        )

    def get_main_content(self):
        name = self._storage.get('manga_name', self.get_manga_name())
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        uri = self.get_url()
        test = self.re.search(r'\.us/read\-online/.+', uri)
        if test:
            uri = self.html_fromstring(uri, 'a.list-link', 0).get('href')
        return self.re.search(r'(?:\.us)?/manga/([^/]+)', uri).group(1)

    def get_chapters(self):
        return self.document_fromstring(self.get_storage_content(), '.chapter-list a.list-group-item')

    def _get_image(self, parser):
        return parser.cssselect('.image-container .CurImage')[0].get('src')

    def get_files(self):
        url = self.get_current_chapter()
        parser = self.html_fromstring(url, '.mainWrapper', 0)
        pages = parser.cssselect('select.PageSelect')[0].cssselect('option + option')
        images = [self._get_image(parser)]
        for page in pages:
            page_url = self.re.sub(r'(.+page\-)\d+(.+)', r'\1{}\2', url)
            parser = self.html_fromstring(page_url.format(page.get('value')))
            images.append(self._get_image(parser))
        return images

    def get_cover(self) -> str:
        return self._get_cover_from_content('.leftImage img')


main = MangaLifeUs
