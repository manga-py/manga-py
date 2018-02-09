from src.provider import Provider


class ReadComicBooksOnlineOrg(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/reader/[^/]+_(\\d+)(/\\d+)?', self.get_current_chapter()).groups()
        return '{}-{}'.format(
            idx[0],
            0 if idx[1] is None else idx[1]
        )

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('\\.(?:org|net)/(?:reader/)?([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        s = '#chapterlist .chapter > a'
        return self.document_fromstring(self.get_storage_content(), s)

    def _get_image(self, parser):
        src = parser.cssselect('a > img.picture')
        if not src:
            return None
        return '{}/reader/{}'.format(self.get_domain(), src[0].get('src'))

    def get_files(self):
        chapter = self.get_current_chapter()
        content = self.html_fromstring(chapter, '.pager select[name="page"]', 0)
        pages = [i.get('value') for i in content.cssselect('option + option')]
        img = self._get_image(content)
        images = []
        img and images.append(img)
        for i in pages:
            _content = self.html_fromstring('{}/{}'.format(chapter, i))
            img = self._get_image(_content)
            img and images.append(img)
        return images


main = ReadComicBooksOnlineOrg
