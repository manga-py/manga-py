from manga_py.provider import Provider
from .helpers.std import Std
from manga_py.crypt import hoducomics_com


class HoduComicsCom(Provider, Std):
    _crypt = None

    def debug(self, content):
        if isinstance(content, str):
            content = content.encode()
        with open('Manga/content.json', 'wb') as f:
            f.write(content)
        exit()

    def get_archive_name(self) -> str:
        return 'ep'

    def get_chapter_index(self) -> str:
        pass

    def get_main_content(self):
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
        return [n(re.search(i.get('onclick')).group(1)) for i in items]

    def get_files(self):
        content = self.http_get(self.chapter)
        images = self.re.search(r'var\s+toon_img\s*=\s*[\'"](.+?)[\'"]', content)
        if not images:
            return []
        parser = self.document_fromstring(self._crypt.base64decode(images.group(1)))

        # DEBUG!
        self.debug(self.json.dumps(self._images_helper(parser, 'img')))

        return self._images_helper(parser, 'img')

    def get_cover(self) -> str:
        return self._cover_from_content('.episode_bnr > img')

    def book_meta(self) -> dict:
        pass

    def prepare_cookies(self):
        self._crypt = hoducomics_com.HoduComicsCom()
        self.cf_protect(self.get_url())


main = HoduComicsCom
