from src.providers.gomanga_co import GoMangaCo


class JapScanCom(GoMangaCo):
    _name_re = r'\.com/[^/]+/([^/]+)/'
    _content_str = '{}/mangas/{}/'
    _chapters_selector = '#liste_chapitres ul li a'

    def get_archive_name(self) -> str:
        idx = self._chapter_index(), self.get_chapter_index()
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = r'\.com/[^/]+/[^/]+/(\d+)/'
        url = self.get_current_chapter()
        return '{}'.format(self.re.search(selector, url))

    def _get_image(self, n, parser):
        return n(parser.cssselect[0].get('#image'))

    def get_files(self):
        n = self.http().normalize_uri
        parser = self.html_fromstring(self.get_current_chapter())
        pages = parser.cssselect('#pages option + option')
        images = [self._get_image(n, parser)]
        for i in pages:
            parser = self.html_fromstring(n(i.get('value')))
            images.append(self._get_image(n, parser))
        return images

    def get_cover(self) -> str:
        pass


main = JapScanCom
