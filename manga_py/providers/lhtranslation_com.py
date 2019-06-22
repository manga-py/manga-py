from time import sleep

from requests import get

from .gomanga_co import GoMangaCo
from .helpers.std import Std


class LHTranslationCom(GoMangaCo, Std):
    _name_re = r'/(?:truyen|manga)-([^/]+)\.html'
    _content_str = '{}/manga-{}.html'
    _chapters_selector = '#tab-chapper td > a.chapter,#list-chapters a.chapter'

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'-chapter-(.+?)\.html', self.chapter)
        return idx.group(1).replace('.', '-')

    def get_files(self):
        content = self.http_get(self.chapter)
        parser = self.document_fromstring(content, 'article#content,.chapter-content', 0)
        return self._images_helper(parser, 'img.chapter-img', 'data-original')


main = LHTranslationCom
