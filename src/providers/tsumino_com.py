from src.provider import Provider
from .helpers.std import Std


class TsuminoCom(Provider, Std):
    __local_storage = None

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_main_content(self):
        url = self.get_url()
        if ~url.find('/Read/'):
            url = self.html_fromstring(url, '#backToIndex + a', 0).get('href')
        return self.http_get(self.http().normalize_uri(url))

    def get_manga_name(self) -> str:
        url = self.get_url()
        if ~url.find('/Read/'):
            url = self.html_fromstring(url, '#backToIndex ~ a', 0).get('href')
        return self.re.search(r'/Info/\d+/([^/]+)', url).group(1)

    def get_chapters(self):
        return [b'']

    def get_files(self):
        idx = self.re.search(r'/(?:Info|View)/(\d+)', self.get_url()).group(1)
        content = self.http_post('{}/Read/Load'.format(self.domain, idx), data={'q': idx})
        items = self.json.loads(content).get('reader_page_urls')
        d = str(self.domain)
        return [d + '/Image/Object?name=' + i for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('img.book-page-image')


main = TsuminoCom
