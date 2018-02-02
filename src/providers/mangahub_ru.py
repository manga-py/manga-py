import html

from src.provider import Provider


class MangaHubRu(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re_search('/read/[^/]+/[^\\d]+(\\d+)/(\\d+)/', self.get_current_chapter()).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        url = '{}/{}'.format(self.get_domain(), self.get_manga_name())
        return self.http_get(url)

    def get_manga_name(self) -> str:
        return self.re_search('\\.ru/([^/]+)/?', self.get_url())

    def get_chapters(self):
        parser = self.document_fromstring(self.get_storage_content(), '.b-catalog-list__name a[href^="/"]')
        domain = self.get_domain()
        return [domain + i.get('href') for i in parser]

    def prepare_cookies(self):
        pass

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter(), '.b-main-container .b-reader__full')
        if not parser:
            return []
        result = parser[0].get('data-js-scans')
        result = self.json.loads(html.unescape(result.replace('\/', '/')))
        domain = self.get_domain()
        return [domain + i['src'] for i in result]

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaHubRu
