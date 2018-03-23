from .helpers.nine_manga import NineHelper
from .helpers.std import Std


class NineMangaCom(NineHelper, Std):
    _local_storage = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index(True).split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self, no_increment=False) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        name = self.get_manga_name(False)
        return self.http_get('{}/manga/{}.html?waring=1'.format(self.domain, name))

    def get_manga_name(self, normalize=True) -> str:
        if not self._local_storage:
            name = self.re_name(self.get_url())
            if name:
                self._local_storage = name.group(1)
            else:
                url = self.html_fromstring(self.get_url(), '.subgiude > li + li > a', 0).get('href')
                self._local_storage = self.re_name(url).group(1)
        return self.normalize_name(self._local_storage, normalize)

    def get_chapters(self):
        result = self._elements('.chapterbox li a.chapter_list_a')
        items = []
        for i in result:
            u = self.re.search(r'(/chapter/.*/\d+)\.html', i.get('href'))
            items.append('{}{}-10-1.html'.format(self.domain, u.group(1)))
        return items

    def get_files(self):
        content = self._get_page_content(self.chapter)
        pages = self.document_fromstring(content, '.changepage #page option + option')
        images = self.get_files_on_page(content)
        for i in pages:
            url = self.http().normalize_uri(i.get('value'))
            content = self._get_page_content(url)
            images += self.get_files_on_page(content)
        return images


main = NineMangaCom
