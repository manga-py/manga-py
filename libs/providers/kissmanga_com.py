from .provider import Provider
from libs.crypt import KissMangaComCrypt


class KissMangaCom(Provider):

    __local_data = {
        'iv': b'a5e8e2e9c2721be0a84ad660c472c1f3',
        'key': b'mshsdf832nsdbash20asdm',
    }

    def get_archive_name(self) -> str:
        return self.re.search('/Manga/[^/]+/([^/\?]+)', self.get_current_chapter()).group(1)

    def get_chapter_index(self) -> str:
        name = self.basename(self.get_current_chapter())
        name = self.re.search('Vol.?(\d+).?Ch.?(\d+)', name).groups()
        return '{}-{}'.format(*name)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/Manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/Manga/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        items = self.html_fromstring(self.get_main_content(), '.listing td a')
        return [self.get_domain() + i.get('href') for i in items]

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def __decrypt_images(self, crypt, key, hexes):
        images = []
        for i in hexes:
            img = crypt.decrypt(self.__local_data['iv'], key, i)
            images.append(img)

        return images

    def get_files(self):
        crypt = KissMangaComCrypt()

        content = self.http_get(self.get_current_chapter())

        # if need change key
        need = self.re.search('\["([^"]+)"\].+chko.?=.?chko', content)
        key = self.__local_data['key']
        if need:
            key += crypt.decode_escape(need.group(1))

        hexes = self.re.findall('lstImages.push\(wrapKA\(["\']([^"\']+?)["\']\)', content)

        if not hexes:
            return []

        images = self.__decrypt_images(crypt, key, hexes)

        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = KissMangaCom
