from math import ceil

from manga_py.provider import Provider
from .helpers.std import Std


class KuMangaCom(Provider, Std):
    __local_storage = None

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.chapter_id)

    def get_chapter_index(self) -> str:
        return '{}'.format(self.chapter_id)

    def get_main_content(self):
        if not self.__local_storage:
            url = self.re.search(r'(.+\.com/manga/\d+)', self.get_url())
            self.__local_storage = self.http_get('%s/' % url.group(1))
        return self.__local_storage

    def get_manga_name(self) -> str:
        selector = r'pagination\(\d+,\'(.+)\',\'pagination\''
        parser = self.re.search(selector, self.content)
        return parser.group(1).strip()

    def __chapters(self, parser):
        items = parser.cssselect('.table h4.title > a')
        chapters = []
        for i in items:
            c = '{}/{}'.format(self.domain, i.get('href'))
            chapters.append(c.replace('/c/', '/leer/'))
        return chapters

    def _chapters_helper(self):
        idx = self.re.search(r'\.com/manga/(\d+)', self.get_url())
        return '{}/manga/{}/p/%d/{}'.format(
            self.domain,
            idx.group(1),
            self.manga_name
        )

    def get_chapters(self):
        selector = r'\'pagination\',\d+,(\d+),(\d+)'
        pages = self.re.search(selector, self.content).groups()
        pages = ceil(float(pages[0]) / float(pages[1]))
        chapters = []
        url_path = self._chapters_helper()
        for i in range(int(pages) - 1):
            parser = self.html_fromstring(url_path % (i + 1))
            chapters += self.__chapters(parser)
            return chapters
        return chapters

    def _get_real_url(self, url):
        location = self.http().requests(url=url, method='head')
        return location.headers.get('Location', url)

    def get_files(self):
        r = self.http().get_redirect_url
        selector = r'(\[\{"npage".+\}\])'
        content = self.http_get(self.chapter)
        items = self.json.loads(self.re.search(selector, content))
        return [r(i.get('imgURL')) for i in items.group(1)]

    def get_cover(self) -> str:
        return self._cover_from_content('.container img.img-responsive')


main = KuMangaCom
