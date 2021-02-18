from manga_py.provider import Provider
from .helpers.std import Std


class SundayWebryCom(Provider, Std):
    cdn_url = None

    def get_archive_name(self) -> str:
        return self.get_chapter_index()  # Hmm..

    def get_chapter_index(self) -> str:
        return self.re.search(r'cti=([^&]*)', self.chapter).group(1)

    def get_content(self):
        return self.http_get('{}/series/{}'.format(
            self.domain,
            self._get_name(r'/series/(\d+)')
        ))

    def get_manga_name(self) -> str:
        return 'sunday_' + self._get_name(r'/series/(\d+)')

    def _chapters(self, content):
        return self._elements('li[id^="product_"] a.button_free', content)

    def get_chapters(self):
        pages = self._elements('.pagination')
        chapters = self._chapters(self.content)
        if pages:
            pages = pages[0].cssselect('a:not([class])')
            n = self.http().normalize_uri
            for i in pages:
                chapters += self._chapters(n(i.get('href')))
        return chapters

    def _prepare_urls(self):
        cid = self.re.search('cid=([^&]+)', self.chapter).group(1)
        license_url = '{}/api4js/contents/license?cid={}'.format(self.domain, cid)
        self.cdn_url = self.json.loads(self.http_get(license_url)).get('url', None)
        items = self.json.loads(self.http_get(self.cdn_url + 'configuration_pack.json'))
        return items.get('configuration', {}).get('contents', [])

    def get_files(self):
        items = []
        for i in self._prepare_urls():
            file = '%s/0.jpeg' % i.get('file')
            items.append(self.cdn_url + file)
        return items

    def after_file_save(self, _path: str, idx: int):  # todo issue #36
        return super().after_file_save(_path, idx)

    def get_cover(self) -> str:
        return self._cover_from_content('#series .image > img')

    def prepare_cookies(self):
        self._base_cookies()

    def book_meta(self) -> dict:
        # todo meta
        pass


main = SundayWebryCom
