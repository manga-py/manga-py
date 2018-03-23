from manga_py.provider import Provider
from .helpers.std import Std


class ReadComicBooksOnlineOrg(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/reader/[^/]+_(\d+(?:/\d+)?)')
        idx = re.search(self.chapter).groups()
        return '-'.join(idx.split('/'))

    def get_main_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.(?:org|net)/(?:reader/)?([^/]+)')

    def get_chapters(self):
        s = '#chapterlist .chapter > a'
        return self.document_fromstring(self.content, s)

    def _get_image(self, parser):
        src = parser.cssselect('a > img.picture')
        if not src:
            return None
        return '{}/reader/{}'.format(self.domain, src[0].get('src'))

    def get_files(self):
        chapter = self.chapter
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

    def get_cover(self):
        pass


main = ReadComicBooksOnlineOrg
