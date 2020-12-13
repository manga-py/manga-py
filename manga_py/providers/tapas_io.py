from manga_py.provider import Provider
from .helpers import tapas_io
from .helpers.std import Std


class TapasIo(Provider, Std):  # TODO: Login\Password
    helper = None

    def get_archive_name(self) -> str:
        ch = self.chapter
        return self.normal_arc_name([
            ch['scene'],
            ch['title']
        ])

    def get_chapter_index(self) -> str:
        return str(self.chapter['scene'])

    def get_content(self):
        content = self._storage.get('main_content', False)
        return content if content else self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.re.search(r'seriesTitle\s*:\s*\'(.+)\',', self.content).group(1)

    def get_chapters(self):
        items = self.re.search(r'episodeList\s*:\s*(\[.+\]),', self.content).group(1)
        return [i for i in self.json.loads(items)[::-1] if not i['locked']]

    def get_files(self):
        return self.helper.parse_chapter_content()

    def get_cover(self) -> str:
        return self._cover_from_content('#series-thumb img')

    def prepare_cookies(self):
        self.helper = tapas_io.TapasIo(self)

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.helper.chapter_url()


main = TapasIo
