from .gomanga_co import GoMangaCo


class GMangaMe(GoMangaCo):
    _name_re = '/mangas/([^/]+)'
    _content_str = '{}/mangas/{}'
    _chapters_selector = 'a.chapter-link'

    def get_chapter_index(self) -> str:
        selector = r'/mangas/[^/]+/(\d+/[^/]+)'
        idx = self.re.search(selector, self.chapter).group(1)
        return idx.replace('/', '-')

    def _get_json_selector(self, content):
        return r'1:\salphanumSort\((\[.+\])\)'

    def get_cover(self) -> str:
        image = self.re.search(r'"image"\s?:\s?"(.+)",', self.content)
        if image:
            return image.group(1)


main = GMangaMe
