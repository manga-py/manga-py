from src.provider import Provider


class MangaSaurusCom(Provider):
    def get_archive_name(self) -> str:
        return 'vol_{:0>3'.format(self._chapter_index())

    def get_chapter_index(self) -> str:
        return str(self._chapter_index())

    def get_main_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        result = self.re.search(r'/manga/(\d+)/([^/]+)', self.get_url()).groups()
        return '{1}_{0}'.format(*result)

    def get_chapters(self):
        c, s = self.get_storage_content(), '.table--chapters td > a'
        return self.document_fromstring(c, s)[::-1]

    def __files_helper(self):
        content = self.http_get(self.get_current_chapter())
        _path = self.document_fromstring(content, '#imageZone-next > img', 0).get('src')
        path = self.re.search('(http.+?/original)/', _path).group(1) + '/{}/{}-{}{}'
        parser = self.re.search(r'ImageReader\.setImages.+?(\{.+\})', content)
        return path, parser

    def get_files(self):
        path, parser = self.__files_helper()
        if not parser:
            return []
        images = []
        o = self.json.loads(parser.group(1))
        for i in o:
            n = o.get(i)
            _ = n.get('original', {}).get('file', '')
            idx = _.find('.')
            src = path.format(_[:idx], self.get_manga_name(), n['id'], _[idx:])
            images.append(src)
        return images


main = MangaSaurusCom
