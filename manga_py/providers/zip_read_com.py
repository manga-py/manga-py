from manga_py.provider import Provider
from .helpers.jav_zip_org import JavZipOrg
from .helpers.std import Std


class ZipReadCom(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/.p=(\d+)', self.chapter).group(1)
        return '{}-{}'.format(self.chapter_id, idx)

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        return self._elements('#content .entry > p > a')

    def get_files(self):
        jav_zip_org = JavZipOrg(self)
        return jav_zip_org.get_images()

    def get_cover(self):
        return self._cover_from_content('#content .entry p > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ZipReadCom
