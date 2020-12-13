from manga_py.provider import Provider
from .helpers.std import Std


class ComicsAndMangaRu(Provider, Std):

    def get_archive_name(self) -> str:
        index = self.get_chapter_index()
        return 'vol_{:0>3}'.format(index)

    def get_chapter_index(self) -> str:
        return self.re.search(r'.+/[^/]+?(\d+)$', self.chapter).group(1)

    def get_content(self):
        name = self.re.search('/(online-reading/[^/]+/[^/]+)', self.get_url())
        return self.http_get('{}/{}'.format(self.domain, name.group(1)))

    def get_manga_name(self):
        name = self.re.search('/online-reading/[^/]+/([^/]+)', self.get_url())
        return name.group(1)

    def get_chapters(self):
        selector = '.MagList > .MagListLine > a'
        items = self.document_fromstring(self.content, selector)
        return items[::-1]

    def get_files(self):
        img_selector = 'a > img'
        nu = self.http().normalize_uri
        uri = nu(self.chapter)
        parser = self.html_fromstring(uri, '.ForRead', 0)
        pages = parser.cssselect('.navigation select')[0].cssselect('option + option')
        images = self._images_helper(parser, img_selector)

        for i in pages:
            uri = '{}/{}'.format(nu(self.chapter.rstrip('/')), i.get('value'))
            parser = self.html_fromstring(uri, '.ForRead', 0)
            images += self._images_helper(parser, img_selector)

        return images

    def get_cover(self):
        pass  # TODO

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ComicsAndMangaRu
