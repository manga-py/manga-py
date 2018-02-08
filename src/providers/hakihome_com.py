from src.provider import Provider


class HakiHomeCom(Provider):

    def get_archive_name(self) -> str:
        return self.get_chapter_index()

    def get_chapter_index(self) -> str:
        selector = '.+/([^/]+)/'
        url = self.get_current_chapter()
        idx = self.re.search(selector, url)
        return idx.group(1)

    def get_main_content(self):
        selector = '(https?://[^/]+/[^/]+/[^/]+\\-\\d+/)'
        url = self.re.search(selector, self.get_url())
        return self.http_get(url.group(1))

    def get_manga_name(self) -> str:
        _ = self.http().normalize_uri('http://s1.hakihome.com/images/eng/C/Cumming inside asuna 100 raw part 1/003.jpg \\r\\n')
        url = self.get_url()
        selector = '\\.com/[^/]+/(.+?)\\-\\d+/'
        return self.re.search(selector, url).group(1)

    def get_chapters(self):
        content = self.get_storage_content()
        selector = '.listing a.readchap'
        items = self.document_fromstring(content, selector)
        return [i.get('href') for i in items]

    def get_files(self):
        n = self.http().normalize_uri
        images = []
        uri = n(self.get_current_chapter())
        parser = self.html_fromstring(uri, '#contentchap', 0)
        pages = parser.cssselect('#botn span > select[onchange] > option + option')
        img = self._images_helper(parser)
        img and images.append(img)

        for i in pages:
            parser = self.html_fromstring(n(i.get('value')), '#contentchap', 0)
            img = self._images_helper(parser)
            img and images.append(img)

        return images

    @staticmethod
    def _images_helper(parser):
        image = parser.cssselect('#con img')
        if len(image):
            return image[0].get('src').strip(' \\r\\n')
        return None

    def get_cover(self) -> str:
        return self._get_cover_from_content('.noidung img')


main = HakiHomeCom
