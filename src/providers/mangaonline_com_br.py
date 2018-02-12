from src.provider import Provider


class MangaOnlineComBr(Provider):

    def get_archive_name(self) -> str:
        return 'vol_{}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        selector = r'\.br/[^/]+/[^/]+/([^/]+)'
        return self.re.search(selector, self.get_current_chapter()).group(1)

    def get_main_content(self):
        params = self.get_domain(), self.get_manga_name()
        return self.http_get('{}/{}/'.format(*params))

    def get_manga_name(self) -> str:
        return self.re.search(r'\.br/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        selector = '#volumes-capitulos span > a'
        return self.document_fromstring(self.get_main_content(), selector)

    def _get_images(self, parser):
        items = parser.cssselect('#imgPadraoVisualizacao img')
        return [i.get('src') for i in items]

    def _get_pages_count(self, parser):
        pages = parser.cssselect('select.pagina-capitulo')
        if pages:
            return len(pages[0].cssselect('option + option'))
        return 0

    def get_files(self):
        url = '{}/capitulo.php?act=getImg&anime={}&capitulo={}&src={}&view=1'
        params = (
            self.get_domain(),
            self.get_manga_name(),
            self.get_chapter_index()
        )
        parser = self.html_fromstring(url.format(*params, 1))
        images = self._get_images(parser)
        pages = self._get_pages_count(parser)
        if pages:
            for i in range(int(pages / 2)):
                parser = self.html_fromstring(url.format(*params, ((i + 1) * 2 + 1)))
                images += self._get_images(parser)

        return images

    def get_cover(self) -> str:
        return self._get_cover_from_content('.image > img')


main = MangaOnlineComBr
