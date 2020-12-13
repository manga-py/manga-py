from manga_py.provider import Provider
from .helpers.std import Std


class ReadComicOnlineTo(Provider, Std):
    def get_archive_name(self) -> str:
        chapter = self.re.search(r'id=(\d+)', self.chapter).group(1)
        return self.normal_arc_name([self.chapter_id, chapter])

    def get_chapter_index(self, no_increment=False) -> str:
        return str(self.chapter_id)

    def get_content(self):
        return self._get_content(r'{}/Comic/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'/Comic/([^/]+)')

    def get_chapters(self):
        return self._elements('table.listing td > a')

    def prepare_cookies(self):
        self.cf_scrape(self.get_url())
        self._storage['cookies']['rco_quality'] = 'hq'

    def get_files(self):
        content = self.http_get(self.chapter + '&readType=1')
        items = self.re.findall(r'lstImages.push\("([^"]+)"\)', content)
        return items

    def get_cover(self):
        return self._cover_from_content('.rightBox .barContent img[width]')


main = ReadComicOnlineTo
