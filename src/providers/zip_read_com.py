from src.provider import Provider
from src.providers.helpers.jav_zip_org import JavZipOrg


class ZipReadCom(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/.p=(\d+)', self.get_current_chapter()).group(1)
        return '{}-{}'.format(self._chapter_index(), idx)

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        return self.re.search(r'\.com/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        return self.html_fromstring(self.get_url(), '#content .entry > p > a')

    def get_files(self):
        jav_zip_org = JavZipOrg(self)
        return jav_zip_org.get_images()


main = ZipReadCom
