from typing import List

from manga_py.libs.provider.file_tuple import *
from manga_py.libs.provider import Provider
from manga_py.libs.provider.std import Std


class ReadMangaMe(Provider, Std):
    @staticmethod
    def supported_urls():
        return [
            r'readmanga.me',
        ]

    def manga_name(self) -> str:
        element = self.elements(self.store.content, '', 0)
        return self.text_content(element)

    def chapters(self) -> List[ChapterTuple]:
        pass

    def chapter_files(self, chapter: ChapterTuple) -> List[ChapterFilesTuple]:
        pass
