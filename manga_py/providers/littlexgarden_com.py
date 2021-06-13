from manga_py.provider import Provider
from .helpers.std import Std


class LittleXGardenCom(Provider, Std):
    __images_webroot = 'https://littlexgarden.com/static/images/'

    def get_chapter_index(self) -> str:
        return self.re.search(r'\.\w{2,5}/[^/]+/(\d+)', self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,5}/([^/]+)')

    def get_chapters(self):
        return self._elements('.chapters > .list a[title]')[::-1]

    def get_files(self):
        content = self.http_get(self.chapter)
        script_content = None

        scripts = self.document_fromstring(content, 'script')

        nuxt_re = self.re.compile(r'__NUXT__\s?=')
        image_re = self.re.compile(r'"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\.jpg)"')

        for script in scripts:
            source = self.element_text_content(script)
            if nuxt_re.search(source):
                script_content = source
                break

        if script_content is None:
            self.log('Images not found')
            return []

        return list(map(self._image_url, image_re.findall(script_content)))

    def _image_url(self, image_id: str):
        if self.http().allow_webp:
            return f'{self.__images_webroot}webp/{image_id}.webp'
        return f'{self.__images_webroot}{image_id}'


main = LittleXGardenCom
