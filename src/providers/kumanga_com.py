from src.provider import Provider
from math import ceil


class KuMangaCom(Provider):
    __local_storage = None

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self._chapter_index())

    def get_chapter_index(self) -> str:
        return '{}'.format(self._chapter_index())

    def get_main_content(self):
        if not self.__local_storage:
            url = self.re.search(r'(.+\.com/manga/\d+)').group(1)
            self.__local_storage = self.http_get('%s/' % url)
        return self.__local_storage

    def get_manga_name(self) -> str:
        parser = self.document_fromstring(self.get_main_content(), '.h1_container h1', 0)
        return parser.text_content().strip()

    def get_chapters(self):
        selector = r'\'pagination\',\d+,(\d+),(\d+)'
        pages = self.re.search(selector, self.get_storage_content()).groups()
        pages = ceil(pages[0]/pages[1])
        print(pages)  # TODO
        exit()
        return []

    def get_files(self):
        selector = r'(\[\{"npage".+\}\])'
        content = self.http_get(self.get_current_chapter())
        items = self.json.loads(self.re.search(selector, content))
        return [i.get('imgURL') for i in items]

    def get_cover(self) -> str:
        return self._get_cover_from_content('.container img.img-responsive')


main = KuMangaCom
