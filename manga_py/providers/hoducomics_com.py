from manga_py.crypt.base_lib import BaseLib
from manga_py.provider import Provider
from .helpers.std import Std


class HoduComicsCom(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name({'vol': [
            self.chapter_id,
            self.get_chapter_index()
        ]})

    def get_chapter_index(self) -> str:
        return self.re.search(r'view/(\d+)', self.chapter).group(1)

    def get_content(self):
        content = self._storage.get('main_content', None)
        if content is None:
            self._storage['main_content'] = self.http_get(self.get_url())
        return self._storage['main_content']

    def get_manga_name(self) -> str:
        self.http().referer = self.get_url()
        element = self.document_fromstring(self.content, '[property="og:title"]', 0)
        return element.get('content')

    def get_chapters(self):
        items = self._elements('.episode_list .episode_tr.not_need_pay')
        re = self.re.compile(r'(/webtoon/.+?/\d+)')
        n = self.http().normalize_uri
        if len(items) == 0:
            return []
        return [n(re.search(i.get('onclick')).group(1)) for i in items]

    def get_files(self):
        content = self.http_get(self.chapter)
        images = self.re.search(r'toon_img\s*=\s*[\'"](.+?)[\'"]', content)
        if not images:
            return []
        parser = self.document_fromstring(BaseLib.base64decode(images.group(1)).decode())
        return self._images_helper(parser, 'img')

    def get_cover(self) -> str:
        return self._cover_from_content('.episode_bnr > img')

    def book_meta(self) -> dict:
        pass

    def prepare_cookies(self):
        self.cf_scrape(self.get_url())


main = HoduComicsCom
