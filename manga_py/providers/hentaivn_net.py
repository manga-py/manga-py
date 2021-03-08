from manga_py.provider import Provider
from .helpers.std import Std


class HentaiVnNet(Provider, Std):
    def get_chapter_index(self) -> str:
        return self.chapter_id

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/\d+(?:-\w+){2}-(.+)\.htm')

    def get_chapters(self):
        return self._elements('.listing a')

    def prepare_cookies(self):
        self.update_cookies({'page_ads_right': '1'})
        self.cf_scrape(self.get_url())

    def get_files(self):
        content = self.http_get(self.chapter)
        parser = self.document_fromstring(content)
        return self._images_helper(parser, '#image img')

    def get_cover(self) -> str:
        return self._cover_from_content('.page-ava img')


main = HentaiVnNet
