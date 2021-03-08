from manga_py.provider import Provider
from .helpers import tsumino_com
from .helpers.std import Std


class TsuminoCom(Provider, Std):
    __local_storage = None

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_content(self):
        url = self.get_url()
        if ~url.find('/Read/'):
            url = self.html_fromstring(url, '#backToIndex + a', 0).get('href')
        return self.http_get(self.http().normalize_uri(url))

    def get_manga_name(self) -> str:
        return 'tsumino_' + self.re.search(r'/(?:Info|View)/(\d+)', self.get_url()).group(1)

    def get_chapters(self):
        return [b'']

    def prepare_cookies(self):
        self._base_cookies()

    def get_files(self):
        idx = self.re.search(r'/(?:Info|View)/(\d+)', self.get_url()).group(1)
        test_url = '{}/Read/View{}'.format(self.domain, idx)
        if ~self.http_get(test_url).find('/recaptcha'):
            cookies = tsumino_com.TsuminoCom(self).get_cookies(test_url).get_dict()
            for i in cookies:
                self._storage['cookies'][i] = cookies[i]

        with self.http().post(
            '{}/Read/Load'.format(self.domain, idx),
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': '{}/Read/View/{}'.format(self.domain, idx),
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Accept-Language': 'en-US;q=0.8,en;q=0.7',
            },
            data={'q': idx}
        ) as resp:
            items = resp.json().get('reader_page_urls', [])
        d = str(self.domain)
        return [d + '/Image/Object?name=' + i for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('img.book-page-image')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = TsuminoCom
