from manga_py.provider import Provider
from .helpers.std import Std


class MangaSaurusCom(Provider, Std):

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        return self.http_get('{}/manga/{}/{}'.format(
            self.domain,
            *self.manga_name.split('_')
        ))

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/view/'):
            url = self.html_fromstring(url, '#m_reader_bottom + div > a', 0).get('href')
        result = self.re.search(r'/manga/(\d+)/([^/]+)', url).groups()
        return '{1}_{0}'.format(*result)

    def get_chapters(self):
        return self._elements('.table--chapters td > a')[::-1]

    def __files_helper(self):
        content = self.http_get(self.chapter)
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
            src = path.format(_[:idx], self.manga_name, n['id'], _[idx:])
            images.append(src)
        return images

    def get_cover(self):
        self._cover_from_content('.gallery-info__cover img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaSaurusCom
