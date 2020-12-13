import urllib3

from manga_py.provider import Provider
from .helpers.std import Std


class MangaTownCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.re.search('/manga/[^/]+(?:/v(\d+))?/c([^/]+)', self.chapter).groups()
        if idx[0]:
            var = {'vol': idx[0], 'ch': idx[1].split('.')}
        else:
            var = {'vol': '0', 'ch': idx[1].split('.')}
        return self.normal_arc_name(var)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/manga/[^/]+(?:/v\d+)?/c([^/]+)', self.chapter)
        return idx.group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/manga/{}/')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)/?')

    def get_chapters(self):
        return self.document_fromstring(self.content, '.chapter_list a')

    def prepare_cookies(self):
        self._storage['domain_uri'] = self.domain.replace('//m.', '//')
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._http_kwargs['verify'] = False

    def get_files(self):
        img_selector = 'img#image'
        url = self.http().normalize_uri(self.chapter)
        parser = self.html_fromstring(url)
        pages = self._first_select_options(parser, '.page_select')
        images = self._images_helper(parser, img_selector)

        for i in pages:
            url = self.http().normalize_uri(i.get('value'))
            img = self.html_fromstring(url)
            images += self._images_helper(img, img_selector)

        return images

    def get_cover(self):
        return self._cover_from_content('.detail_info > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaTownCom
