import urllib3

from manga_py.provider import Provider
from .helpers.std import Std


class MangaTownCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/manga/[^/]+/c([^/]+)', self.chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        return self._get_content('{}/manga/{}/')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)/?')

    def get_chapters(self):
        return self.document_fromstring(self.content, '.chapter_list a')

    def prepare_cookies(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._http_kwargs['verify'] = False

    def get_files(self):
        img_selector = 'img#image'
        url = self.http().normalize_uri(self.chapter)
        parser = self.html_fromstring(url)
        selector = '#top_chapter_list + .page_select select option + option'
        images = self._images_helper(parser, img_selector)

        for i in parser.cssselect(selector):
            url = self.http().normalize_uri(i.get('value'))
            img = self.html_fromstring(url)
            images += self._images_helper(img, img_selector)

        return images

    def get_cover(self):
        return self._cover_from_content('.detail_info > img')


main = MangaTownCom
