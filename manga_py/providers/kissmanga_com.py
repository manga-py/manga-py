from manga_py.crypt import KissMangaComCrypt
from manga_py.fs import basename
from manga_py.provider import Provider
from .helpers.std import Std


class KissMangaCom(Provider, Std):
    __local_data = {
        'iv': b'a5e8e2e9c2721be0a84ad660c472c1f3',
        'key': b'mshsdf832nsdbash20asdm',
    }

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'Ch-{:0>3}_Vol-{:0>3}-{:0>1}'.format(*idx.split('-'))

    def get_chapter_index(self) -> str:
        bn = basename(self.chapter)
        name = self.re.search(r'Vol-+(\d+)-+Ch\w*?-+(\d+)-+(\d+)', bn)
        if name:
            name = name.groups()
            return '{1}-{0}-{2}'.format(*name)
        name = self.re.search(r'Vol-+(\d+)-+Ch\w*?-+(\d+)', bn)
        if name:
            name = name.groups()
            return '{1}-{0}-0'.format(*name)
        name = self.re.search(r'Ch\w+-*(\d+)', bn).group(1)
        return '{}-{}-0'.format(name, '0' * len(name))

    def get_main_content(self):
        return self._get_content('{}/Manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/Manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.listing td a')

    def prepare_cookies(self):
        self.cf_protect(self.get_url())
        self._storage['cookies']['rco_quality'] = 'hq'

    def __decrypt_images(self, crypt, key, hexes):
        images = []
        for i in hexes:
            img = crypt.decrypt(self.__local_data['iv'], key, i)
            images.append(img)

        return images

    def get_files(self):
        crypt = KissMangaComCrypt()

        content = self.http_get(self.chapter)

        # if need change key
        need = self.re.search(r'\["([^"]+)"\].+chko.?=.?chko', content)
        key = self.__local_data['key']
        if need:
            key += crypt.decode_escape(need.group(1))

        hexes = self.re.findall(r'lstImages.push\(wrapKA\(["\']([^"\']+?)["\']\)', content)

        if not hexes:
            return []

        images = self.__decrypt_images(crypt, key, hexes)

        return [i.replace('\x10', '') for i in images]

    def get_cover(self):
        return self._cover_from_content('.rightBox .barContent img')


main = KissMangaCom
