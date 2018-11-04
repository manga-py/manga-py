from manga_py.crypt import KissMangaComCrypt
from manga_py.provider import Provider
from .helpers.std import Std

from sys import stderr


class KissMangaCom(Provider, Std):
    __local_data = {
        'iv': b'a5e8e2e9c2721be0a84ad660c472c1f3',
        'key': b'mshsdf832nsdbash20asdm',
    }

    def get_archive_name(self) -> str:
        return '{:0>3}-{}'.format(
            self.chapter_id + 1,
            self.get_chapter_index()
        )

    def get_chapter_index(self) -> str:
        name = self.re.search(r'/Manga/[^/]+/(.+)\?id=(\d+)', self.chapter)
        return '-'.join(name.groups())

    def get_main_content(self):
        return self._get_content('{}/Manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/Manga/([^/]+)')

    def get_chapters(self):
        chapters = self._elements('.listing td a')
        if not len(chapters):
            print('Chapters not found', file=stderr)
        return chapters

    def prepare_cookies(self):
        self._params['rename_pages'] = True
        self.cf_protect(self.get_url())
        self._storage['cookies']['rco_quality'] = 'hq'
        if not self._params['cf-protect']:
            print('CloudFlare protect fail!', file=stderr)

    def __decrypt_images(self, crypt, key, hexes):
        images = []
        for i in hexes:
            try:
                img = crypt.decrypt(self.__local_data['iv'], key, i)
                images.append(img.decode('utf-8', errors='ignore').replace('\x10', '').replace('\x0f', ''))

            except Exception as e:
                pass

        return images

    def __check_key(self, crypt, content):
        # if need change key
        need = self.re.search(r'\["([^"]+)"\].\+chko.?=.?chko', content)
        key = self.__local_data['key']
        if need:
            # need last group
            key += crypt.decode_escape(need.group(1))
        else:
            # if need change key
            need = self.re.findall(r'\["([^"]+)"\].*?chko.*?=.*?chko', content)
            if need:
                key = crypt.decode_escape(need[-1])
        return key

    def get_files(self):
        crypt = KissMangaComCrypt()
        content = self.http_get(self.chapter)
        key = self.__check_key(crypt, content)
        hexes = self.re.findall(r'lstImages.push\(wrapKA\(["\']([^"\']+?)["\']\)', content)
        if not hexes:
            print('Images not found!', file=stderr)
            return []
        self._storage['referer'] = self.http().referer = ''
        return self.__decrypt_images(crypt, key, hexes)

    def get_cover(self):
        return self._cover_from_content('.rightBox .barContent img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = KissMangaCom
