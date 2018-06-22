from manga_py.provider import Provider
from .helpers.std import Std


class HGameCGCom(Provider, Std):
    __img_selector = '#thumbnails > div .col-thumbnail'
    __img_count = 0

    def get_archive_name(self) -> str:
        return 'page_{:0>3}'.format(self.chapter)

    def get_chapter_index(self) -> str:
        return '0'

    def get_main_content(self):
        return self._get_content('{}/index/category/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/index/category/([^/]+)')

    def get_chapters(self):
        images = self.document_fromstring(self.content, self.__img_selector)
        self.__img_count = len(images)
        pages = self.document_fromstring(self.content, '.pagination li > a')
        pages_count = 0
        if pages:
            pages_count = self.re.search('/start-(\d+)', pages[-1].get('href')).group(1)
            pages_count = int(int(pages_count) / self.__img_count)
        return range(1, pages_count + 2)[::-1]

    def __tmb_to_img(self, tmbs):
        url = '{}/action.php?id={}&part=e'
        imgs = []
        re = self.re.compile(r'/picture/(\d+)')
        for i in tmbs:
            idx = re.search(i.get('href')).group(1)
            imgs.append(url.format(self.domain, idx))
        return imgs

    def get_files(self):
        pages_url = self.get_url() + '/start-{}'
        if self.chapter > 1:
            offset = self.__img_count * (self.chapter - 1)
            images = self.html_fromstring(pages_url.format(offset), self.__img_selector)
        else:
            images = self.document_fromstring(self.content, self.__img_selector)
        return self.__tmb_to_img(images)

    def get_cover(self) -> str:
        # return self._cover_from_content('.cover img')
        pass

    def book_meta(self) -> dict:
        pass

    def chapter_for_json(self):
        return self.get_url()


main = HGameCGCom
