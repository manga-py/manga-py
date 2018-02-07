from src.provider import Provider


class ComicsAndMangaRu(Provider):

    def get_archive_name(self) -> str:
        index = self.get_chapter_index()
        return 'vol_{:0>3}'.format(index)

    def get_chapter_index(self) -> str:
        return self.re.search('.+/[^/]+?(\\d+)$', self.get_current_chapter()).group(1)

    def get_main_content(self):
        name = self.re.search('/(online-reading/[^/]+/[^/]+)', self.get_url())
        return self.http_get('{}/{}'.format(self.get_domain(), name.group(1)))

    def get_manga_name(self):
        name = self.re.search('/online-reading/[^/]+/([^/]+)', self.get_url())
        return name.group(1)

    def get_chapters(self):
        items = self.document_fromstring(self.get_storage_content(), '.MagList > .MagListLine > a')
        print(len(items))
        return [i.get('href') for i in items[::-1]]

    def get_files(self):
        images = []
        uri = self.get_domain() + self.get_current_chapter()
        parser = self.html_fromstring(uri, '.ForRead', 0)
        pages = parser.cssselect('.navigation select')[0].cssselect('option + option')
        img = self._images_helper(parser)
        img and images.append(img)

        for i in pages:
            uri = '{}/{}/{}'.format(self.get_domain(), self.get_current_chapter().rstrip('/'), i.get('value'))
            parser = self.html_fromstring(uri, '.ForRead', 0)
            img = self._images_helper(parser)

            img and images.append(img)

        return images

    @staticmethod
    def _images_helper(parser):
        image = parser.cssselect('a > img')
        if len(image):
            return image[0].get('src')
        return None


main = ComicsAndMangaRu
