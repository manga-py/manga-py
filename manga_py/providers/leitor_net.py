from manga_py.provider import Provider
from .helpers.std import Std


class LeitorNet(Provider, Std):
    __idx = None

    def get_archive_name(self) -> str:
        ch = self.chapter
        return self.normal_arc_name({
            'vol': ch['number'].split('.'),
            'ch': [ch['id_chapter'], ch['id_release']],
        })

    def get_chapter_index(self) -> str:
        return '-'.join(self.chapter['number'].split('.'))

    def get_content(self):
        idx = self.html_fromstring(self.get_url(), '[data-id-serie]', 0)
        self.__idx = idx.get('data-id-serie')
        return b'0'

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga/([^/]+)')

    @staticmethod
    def __morph_chapters(items):
        result = []
        for item in items:  # items loop
            for r in item['releases']:  # items.releases loop
                release = item['releases'][r]
                result.append({
                    'number': item['number'],
                    'id_chapter': item['id_chapter'],
                    'id_serie': item['id_serie'],
                    'id_release': release['id_release'],
                    'link': release['link'],
                })
        return result

    def get_chapters(self):
        url = '{}/series/chapters_list.json?page={}&id_serie={}'
        items = []
        for i in range(1, 100):
            content = self.json.loads(self.http_get(url.format(
                self.domain, i, self.__idx
            ), headers={'x-requested-with': 'XMLHttpRequest'}))
            chapters = content.get('chapters', False)
            if not chapters:
                break
            items += chapters
        return self.__morph_chapters(items)

    def get_files(self):
        content = self.http_get(self.domain + self.chapter['link'])
        token = self.re.search(r'token=([^&]+)', content).group(1)
        url = '{}/leitor/pages.json?key={}&id_release={}'
        images = self.json.loads(self.http_get(url.format(
            self.domain,
            token, self.chapter['id_release']
        ), headers={'x-requested-with': 'XMLHttpRequest'}))
        return images.get('images', {})

    def get_cover(self) -> str:
        url = '{}/manga/{}/{}'.format(
            self.domain,
            self.manga_name,
            self.__idx
        )
        image = self.html_fromstring(url, '.cover-image')
        if image and len(image):
            return self.parse_background(image[0])

    def book_meta(self) -> dict:
        pass

    def chapter_for_json(self):
        return self.domain + self.chapter['link']


main = LeitorNet
