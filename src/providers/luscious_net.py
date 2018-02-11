from src.provider import Provider


class LusciousNet(Provider):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return str(self.get_chapter_index())

    def get_main_content(self):
        name = self.re.search('/albums?/([^/]+)/', self.get_url()).group(1)
        return self.http_get('{}/albums/{}/'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/albums?/([^/]+)_\d+/', self.get_url()).group(1)

    def get_chapters(self):
        return [b'']

    def get_files(self):
        url = self.get_current_chapter()
        items = self.html_fromstring(url, '#album_meta_ds .item > a')
        n = self.http().normalize_uri
        images = []
        for i in items:
            content = self.http_get(n(i.get('href')), headers={'x-requested-with': 'XMLHttpRequest'})
            image = self.document_fromstring(content, '#single_picture')
            if image:
                images.append(n(image[0].get('src')))
        return images

    def get_cover(self) -> str:
        return self._get_cover_from_content('.album_cover_item img')


main = LusciousNet
