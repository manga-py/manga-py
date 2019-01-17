from manga_py.provider import Provider
from .helpers.std import Std


class SevenSamaCom(Provider, Std):

    def get_archive_name(self) -> str:
        self._vol_fill = True
        name = self.re.sub('[^a-zA-Z0-9]+', '_', self.chapter['chapter_name'])
        return self.normal_arc_name([
            self.chapter['number'],
            str(self.chapter_id),
            name
        ])

    def get_chapter_index(self) -> str:
        return self.chapter_id

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        idx = self.re.search(r'/manga/.+?/(\d+)', self.get_url()).group(1)
        chapters = []
        for i in range(1, 1000):
            content = self.http_get('{}/series/chapters_list.json?page={}&id_serie={}'.format(
                self.domain, i, idx
            ), {'x-requested-with': 'XMLHttpRequest'})
            data = self.json.loads(content)
            if data['chapters'] is False:
                break
            chapters += self.__prepare_chapters(data['chapters'])
        return chapters

    @staticmethod
    def __prepare_chapters(items):
        chapters = []
        for i in items:
            for k, j in i['releases'].items():
                chapter = i.copy()
                chapter['release'] = j
                chapter['release_id'] = k
                chapters.append(chapter)
        return chapters

    def get_files(self):
        url = self.chapter_for_json()
        content = self.http_get('{}{}'.format(self.domain, url))
        api_key = self.re.search(r'this\.page\.identifier\s*=\s*[\'"](.+)[\'"]', content).group(1)
        url = '{}/leitor/pages/{}.json?key={}'.format(
            self.domain, self.chapter['release']['id_release'], api_key
        )
        images = self.json.loads(self.http_get(url, {'x-requested-with': 'XMLHttpRequest'}))
        return images['images']

    def get_cover(self) -> str:
        return self._cover_from_content('.cover img.cover')

    def book_meta(self) -> dict:
        pass

    def chapter_for_json(self) -> str:
        return self.chapter['release']['link']


main = SevenSamaCom
