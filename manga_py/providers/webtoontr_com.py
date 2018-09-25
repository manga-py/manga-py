from .gomanga_co import GoMangaCo
from .helpers.std import Std


class WebtoonTrCom(GoMangaCo, Std):
    _name_re = '/_/([^/]+)'
    _content_str = '{}/_/{}'
    _chapters_selector = '.panel-default table td > a'

    def get_chapter_index(self) -> str:
        url = self.chapter
        index_re = r'/_/[^/]+/(.+)'
        return self.re.search(index_re, url).group(1).replace('.', '-')

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'img.cImg')

    def get_cover(self) -> str:
        return self._cover_from_content('.left img.image')


main = WebtoonTrCom
