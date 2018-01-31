from libs.provider import Provider


class MangaSaurusCom(Provider):
    __local_storage = 0

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index(True).split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self, no_increment=False) -> str:
        idx = '{}-0'.format(self.__local_storage)
        if not no_increment:
            self.__local_storage += 1
        return idx

    def get_main_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        result = self.re_search('\\.com/manga/(\\d+)/([^/]+)', self.get_url()).groups()
        return '{1}_{0}'.format(*result)

    def get_chapters(self):
        parser = self.document_fromstring(self.get_storage_content(), '.table--chapters td > a')
        return [self.get_domain() + i.get('href') for i in parser[::-1]]

    def prepare_cookies(self):
        pass

    def __files_helper(self):
        content = self.http_get(self.get_current_chapter())
        _path = self.document_fromstring(content, '#imageZone-next > img', 0).get('src')
        path = self.re_search('(http.+?/original)/', _path).group(1) + '/{}/{}-{}{}'
        parser = self.re_search('ImageReader\\.setImages.+?(\\{.+\\})', content)
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
            src = path.format(_[0:idx], self.get_manga_name(), n['id'], _[idx:])
            images.append(src)
        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaSaurusCom
