from .comico_co_id_titles import ComicoCoIdTitles
from .helpers.std import Std


class ComicoCoIdContent(ComicoCoIdTitles, Std):  # maybe
    __origin_url = None

    def get_archive_name(self) -> str:
        return '0'

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/title/(\d+)')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        idx = self.re.search(r'contentId=(\d+)', self.get_url())
        return self.http_get('{}/content?contentId={}'.format(
            self.domain,
            idx.group(1)
        ))

    def get_manga_name(self) -> str:
        return 'Fake'

    def prepare_cookies(self):
        self.__origin_url = self.get_url()

    def get_chapters(self):
        pass
        # return self._elements('.contlst-container .contlst-item > a')

    def get_files(self):
        return []

    def get_cover(self) -> str:
        pass

    def chapter_for_json(self):
        return self.get_url()


main = ComicoCoIdContent
