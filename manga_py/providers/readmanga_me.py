import re
from typing import Union, List

from manga_py.libs.base.meta import Meta
from manga_py.provider import Provider


class ReadmangaMe(Provider):
    def get_main_page_url(self) -> str:
        name = re.search(r'\.\w{2,4}/([^/]+)', self.url).group(1)
        return '{}/{}?mature=1&mtr=1'.format(self.domain, name)

    def get_content(self):
        return self.http.get(self.main_page_url)

    def get_manga_name(self) -> str:
        pass

    def get_chapters(self) -> list:
        pass

    def get_files(self) -> list:
        pass

    def get_chapter_name(self) -> Union[list, tuple]:
        pass

    def get_cover(self) -> str:
        pass

    def get_meta(self) -> Meta:
        pass

    def search(self, title: str) -> List[str]:
        pass


main = ReadmangaMe  # Required!
