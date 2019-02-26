from .gomanga_co import GoMangaCo
from .helpers.std import Std


class _Template(GoMangaCo, Std):
    _name_re = r'/manga-([^/]+)\.html'
    _content_str = '{}/manga-{}.html'
    _chapters_selector = '#tab-chapper td > a.chapter'

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'-chapter-(.+?)\.html', self.chapter)
        return idx.group(1).replace('.', '-')

    def get_files(self):
        content = self.http_get(self.chapter)
        parser = self.document_fromstring(content, '.chapter-content', 0)
        return self._images_helper(parser, 'img.chapter-img', 'data-original')


main = _Template
