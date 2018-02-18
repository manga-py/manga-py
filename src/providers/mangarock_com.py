from src.crypt.manga_rock_com_crypt import MangaRockComCrypt
from src.fs import rename, unlink, basename
from src.provider import Provider
from .helpers.std import Std


class MangaRockCom(Provider, Std):
    crypt = None
    __api_uri = 'https://api.mangarockhd.com/query/web400/'

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return str(self._chapter_index())

    def get_main_content(self):
        idx = self.re.search('/manga/([^/]+)', self.get_url())
        return idx.group(1)

    def get_manga_name(self) -> str:
        idx = self.re.search(r'/manga/([^/]+)-\d+', self.get_url())
        return idx.group(1)

    def get_chapters(self):
        idx = self.re.search('/manga/([^/]+)', self.get_url()).group(1)
        url = '{}info?oid={}&last=0&country=Japan'.format(self.__api_uri, idx)
        items = self.json.loads(self.http_get(url))
        return [i.get('oid').encode() for i in items.get('data', {}).get('chapters', [])]

    def get_files(self):
        url = '{}pages?oid={}&country=Japan'.format(self.__api_uri, self.get_current_chapter().decode())
        items = self.json.loads(self.http_get(url))
        return items.get('data')

    # decrypt
    def _loop_callback_files(self, _path):
        _path_wp = _path + 'wp'
        file_r = open(_path, 'rb')
        file_w = open(_path_wp, 'wb')
        file_w.write(self.crypt.decrypt(file_r.read()))
        file_r.close()
        file_w.close()
        unlink(_path)
        rename(_path_wp, _path)

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        _path, idx, _url = self._save_file_params_helper(url, idx)
        in_arc_name = basename(_path) + '.webp'
        return super().save_file(idx, callback, _url, in_arc_name)

    def get_cover(self) -> str:
        selector = 'div:not([class]) > div[class] > div[class] > div[class] > div[class] > img'
        return self._cover_from_content(selector)

    def prepare_cookies(self):
        self.crypt = MangaRockComCrypt()


main = MangaRockCom
