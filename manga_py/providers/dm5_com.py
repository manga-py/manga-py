from manga_py.provider import Provider
from .helpers.std import Std


class Dm5Com(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'[^\d+](\d+)')
        return re.search(self.chapter[1]).group(1)
        pass

    def get_main_content(self):
        content = self._storage.get('main_content', None)
        if content is None:
            if self.get_url().find('/manhua-'):
                # normal url
                name = self._get_name('/manhua-([^/]+)')
            else:
                # chapter url
                selector = '.title .right-arrow > a'
                name = self.html_fromstring(self.get_url(), selector, 0)
                name = self._get_name('/manhua-([^/]+)', name.get('href'))
            content = self.http_get('{}/manhua-{}/'.format(
                self.domain,
                name
            ))
        return content

    def get_manga_name(self) -> str:
        title = self.text_content(self.content, '.info .title')
        if title:
            return title
        re = self.re.search('/manhua-([^/]+)', self.get_url())
        return re.group(1)

    def get_chapters(self):
        items = self._elements('ul.detail-list-select')
        if not items:
            return []
        items = items[0].cssselect('li > a')
        return [(i.get('href'), i.text_content()) for i in items]

    def get_files(self):  # todo
        return []

    def get_cover(self) -> str:
        return self._cover_from_content('.banner_detail_form .cover > img')

    def book_meta(self) -> dict:
        rating = self.text_content(self.content, '.right .score', 0)
        rating = self.re.search(r'(\d\d?\.\d)', rating).group(1)
        author = self.text_content(self.content, '.banner_detail_form .info .subtitle a')
        anno = self.text_content(self.content, '.banner_detail_form .info .content')
        return {
            'author': author,
            'title': self.get_manga_name(),
            'annotation': anno,
            'keywords': str,
            'cover': self.get_cover(),
            'rating': rating,
        }


main = Dm5Com
