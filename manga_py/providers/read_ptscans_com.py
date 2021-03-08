from manga_py.provider import Provider
from .helpers.std import Std


class ReadPtscansCom(Provider, Std):
    def get_chapter_index(self) -> str:
        chapter = self.chapter['title']
        return self.re.search(r'.+?(\d+(?:\.\d+)?)\s*$', chapter)\
            .group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/series/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/series/([^/]+)')

    def get_chapters(self):
        elements = self._elements('.mdc-list-item .mdc-list-item__text > a')

        if len(elements) == 0:
            return []

        content = self.http_get(self.http().normalize_uri(elements[0].get('href')))
        re = self.re.search(r'"(/api/chapters.json.+?)"', content).group(1)
        with self.http().get(self.http().normalize_uri(re)) as resp:
            images = resp.json()
        return images['results']

    def get_files(self):
        with self.http().get(self.http().normalize_uri(self.chapter['manifest'])) as resp:
            json = resp.json()['readingOrder']

        return [i['href'] for i in json]

    def get_cover(self) -> str:
        return self._cover_from_content('.mdc-layout-grid__cell > img')

    def chapter_for_json(self) -> str:
        return self.chapter['title']


main = ReadPtscansCom
