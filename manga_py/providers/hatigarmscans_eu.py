from .gomanga_co import GoMangaCo


class HatigarmScansEu(GoMangaCo):
    _name_re = '/manga/([^/]+)'
    _content_str = '{}/manga/{}/'
    _chapters_selector = '.chapters [class^="chapter-title"] a'

    def get_chapter_index(self) -> str:
        url = self.chapter
        index_re = r'/manga/[^/]+/(\d+(?:\.\d+)?)'
        group = self.re.search(index_re, url).group(1)
        return group.replace('.', '-')

    def prepare_cookies(self):
        pass

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '#all .img-responsive', 'data-src')


main = HatigarmScansEu
