import re
import json
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
        parser = self.html.from_content(self.content)
        return self.html.text_content(parser, '.name')

    def get_chapters(self) -> list:
        return self.html.from_content(self.content, '.chapters-link td > a')

    def get_files(self) -> list:
        content = self.http.get(self.chapter).content
        images = re.search(r'\.init\(\s*(\[.+\])\s*,', content).group(1)
        return [i[1] + i[2] for i in json.load(images.replace('\'', '"'))]

    def get_chapter_name(self) -> Union[str, list, tuple]:
        _re = r'/.+/(?:vol)?([^/]+/[^/]+)(?:/|\?ma?t)?'
        name = re.search(_re, self.chapter).group(1)
        # TODO: need a standard for the name
        return name

    def get_cover(self) -> Union[str, list]:
        parser = self.html.from_content(self.content)
        return self.html.attribute_values(
            parser,
            '.picture-fotorama [data-full]',
            'data-full'
        )

    def get_meta(self) -> Meta:
        parser = self.html.from_content(self.content)
        return Meta(
            authors=[i.text.strip() for i in self.html.elements(parser, '.elem_author > a')],
            year=self.html.text_content(parser, '.elem_year > a'),
            description=self.html.text_content(parser, '.manga-description > p'),
            rating=(float(parser.cssselect('.rating-block').get('data-score')) * 2),
            title=self.html.text_content(parser, '.original-name'),
        )

    def search(self, title: str) -> List[str]:
        items = []
        for item in self.html.from_content(
            self.http.post(
                '{}/search'.format(self.domain),
                {'q': title}
            )
        ):
            items.append(self.http.normalize_uri(item.get('href')))
        return items


main = ReadmangaMe
