from manga_py.crypt import MangaRockComCrypt
from manga_py.fs import rename, unlink, basename
from manga_py.provider import Provider
from .helpers.std import Std


class MangaRockCom(Provider, Std):
    __name = None
    crypt = None
    __api_uri = 'https://api.mangarockhd.com/query/web400/'

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        self.__name = self._get_name(r'/manga/([^/]+-\d+)')
        content = self.http_get('{}/manga/{}'.format(
            self.domain,
            self.__name
        ))
        return self.text_content(content, 'h1')

    def get_chapters(self):
        idx = self._get_name('/manga/([^/]+)')
        url = '{}info?oid={}&last=0&country=Japan'.format(self.__api_uri, idx)
        items = self.json.loads(self.http_get(url))
        return [(i.get('oid'),) for i in items.get('data', {}).get('chapters', [])][::-1]

    def __get_url(self):
        return '{}pages?oid={}&country=Japan'.format(self.__api_uri, self.chapter[0])

    def get_files(self):
        items = self.json.loads(self.http_get(self.__get_url()))
        return items.get('data')

    # decrypt
    def after_file_save(self, _path, idx: int):
        _path_wp = _path + 'wp'
        with open(_path, 'rb') as file_r:
            with open(_path_wp, 'wb') as file_w:
                file_w.write(self.crypt.decrypt(file_r.read()))
        unlink(_path)
        rename(_path_wp, _path)

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        _path, idx, _url = self._save_file_params_helper(url, idx)
        in_arc_name = basename(_path) + '.webp'
        return super().save_file(idx, callback, _url, in_arc_name)

    def get_cover(self) -> str:
        selector = 'div:not([class]) > div[class] > div[class] > div[class] > div[class] > img'
        url = '{}{}'.format(self.domain, self._get_name('(/manga/[^/]+)'))
        img = self._elements(selector, self.http_get(url))
        if img and len(img):
            return img[0].get('src')

    def prepare_cookies(self):
        self.crypt = MangaRockComCrypt()

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = MangaRockCom
