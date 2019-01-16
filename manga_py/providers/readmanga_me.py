import json
import re
from typing import Union, List
from requests import Response

from lxml.etree import ElementBase

from manga_py.libs import fs
from manga_py.libs.html import Html
from manga_py.libs.base.manga import Manga
from manga_py.libs.http import Http
from manga_py.libs.meta import Chapter
from manga_py.provider import Provider


class ReadmangaMe(Provider):
    def get_main_page_url(self) -> str:
        name = re.search(r'\.\w{2,4}/([^/]+)', self.url).group(1)
        return '{}/{}?mature=1&mtr=1'.format(self.domain, name)

    def get_content(self) -> Response:
        return self.http.get(self.main_page_url)

    def get_manga_name(self) -> str:
        parser = self.html.from_content(self.content)
        return self.html.text_content(parser, '.name')

    def get_chapters(self) -> List[dict]:
        items = self.html.from_content(self.content, '.chapters-link td > a')
        result = []
        for idx, item in enumerate(items):  # type: int, ElementBase
            chapter = Chapter(self, idx)
            chapter.name = fs.remove_query(fs.basename(item))
            result.append(chapter)
        return result

    def get_files(self) -> list:
        content = self.http.get(self.chapter.get('url')).content
        images = re.search(r'\.init\(\s*(\[.+\])\s*,', content).group(1)
        return [i[1] + i[2] for i in json.load(images.replace('\'', '"'))]

    def get_chapter_name(self, chapter) -> str:
        _re = r'/.+/(?:vol)?([^/]+/[^/]+)(?:/|\?ma?t)?'
        name = ''  # re.search(_re, self.chapter.url).group(1)
        # TODO: need a standard for the name
        print(name, self.chapter)
        exit()
        return name

    def get_cover(self) -> Union[str, list]:
        parser = self.html.from_content(self.content)
        return self.html.attribute_values(
            parser,
            '.picture-fotorama [data-full]',
            'data-full'
        )

    def get_meta(self) -> Manga:
        parser = self.html.from_content(self.content)

        authors = [i.text.strip() for i in self.html.elements(parser, '.elem_author > a')]

        year = int(self.html.text_content(parser, '.elem_year > a'))

        description = self.html.text_content(parser, '.manga-description > p')

        rating = (float(parser.cssselect('.rating-block').get('data-score')) * 2)

        title = self.html.text_content(parser, '.original-name')

        return Manga(
            authors=authors,
            year=year,
            description=description,
            rating=rating,
            title=title,
        )

    @staticmethod
    def search(title: str, http: Http) -> List[str]:
        items = []
        html = Html(http)
        for item in html.from_content(http.post(
            'http://readmanga.me//search',
            {'q': title}
        )):
            items.append(http.normalize_uri(item.get('href')))
        return items


main = ReadmangaMe
