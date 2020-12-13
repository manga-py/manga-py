from manga_py.provider import Provider
from .helpers.std import Std


class MangaOnlineComBr(Provider, Std):

    def get_chapter_index(self) -> str:
        selector = r'\.\w{2,7}/[^/]+/[^/]+/([^/]+)'
        return self.re.search(selector, self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)')

    def get_chapters(self):
        return self._elements('#volumes-capitulos span > a')

    @staticmethod
    def _get_pages_count(parser):
        pages = parser.cssselect('select.pagina-capitulo')
        if pages:
            return len(pages[0].cssselect('option + option'))
        return 0

    def get_files(self):
        img_selector = '#imgPadraoVisualizacao img'
        url = '{}/capitulo.php?act=getImg&anime={}&capitulo={}&src={}&view=1'
        params = (
            self.domain,
            self.manga_name,
            self.get_chapter_index()
        )
        parser = self.html_fromstring(url.format(*params, 1))
        images = self._images_helper(parser, img_selector)
        pages = self._get_pages_count(parser)
        if pages:
            for i in range(int(pages / 2)):
                parser = self.html_fromstring(url.format(*params, ((i + 1) * 2 + 1)))
                images += self._images_helper(parser, img_selector)

        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.image > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaOnlineComBr
