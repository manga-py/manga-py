from typing import NamedTuple, List, Optional

__all__ = ['Page', 'ComicInfo']


class Page(NamedTuple):
    index: Optional[int]
    size: Optional[int]
    width: Optional[int]
    height: Optional[int]


keys = {
    'title': 'Title',
    'series': 'Series',
    'number': 'Number',
    'volume': 'Volume',
    'alternate_series': 'AlternateSeries',
    'series_group': 'SeriesGroup',
    'summary': 'Summary',
    'notes': 'Notes',
    'year': 'Year',
    'month': 'Month',
    'day': 'Day',
    'writer': 'Writer',
    'penciller': 'Penciller',
    'inker': 'Inker',
    'colorist': 'Colorist',
    'letterer': 'Letterer',
    'cover_artist': 'CoverArtist',
    'editor': 'Editor',
    'publisher': 'Publisher',
    'genre': 'Genre',
    'web': 'Web',
    'page_count': 'PageCount',
    'language': 'Language',
    'iso': 'ISO',
    'age_rating': 'AgeRating',
    'characters': 'Characters',
    'teams': 'Teams',
    'scan_information': 'ScanInformation',
}


class ComicInfo:
    __slots__ = ('__data', '__pages', '_keys')

    def __init__(self):
        self.__data = {
            'title': None,
            'series': None,
            'number': None,
            'volume': None,
            'alternate_series': None,
            'series_group': None,
            'summary': None,
            'notes': None,
            'year': None,
            'month': None,
            'day': None,
            'writer': None,
            'penciller': None,
            'inker': None,
            'colorist': None,
            'letterer': None,
            'cover_artist': None,
            'editor': None,
            'publisher': None,
            'genre': None,
            'web': None,
            'page_count': None,
            'language': None,
            'iso': None,
            'age_rating': None,
            'characters': None,
            'teams': None,
            'scan_information': None,
        }

        self.__pages = []

    def __str__(self):
        schema = 'http://www.w3.org/2001/XMLSchema'
        lines = [
            '<?xml version="1.0"?>',
            f'<ComicInfo xmlns:xsd="{schema}" xmlns:xsi="{schema}-instance">'
        ]
        for key in self.__data.keys():
            if self.__data[key] is None:
                continue

            index = keys[key]
            value = self.__data[key]

            lines.append(f'  <{index}>{value}</{index}>')

        lines.append('    <Pages>')
        pages = sorted(self.__pages, key=lambda p: (p.index or 0))
        for idx, page in enumerate(pages):  # type: int, Page
            _data = ''
            if page.index == 0:
                _data += ' Type="FrontCover"'

            if page.width is not None and page.height is not None:
                _data += f' ImageWidth="{page.width}" ImageHeight="{page.height}"'

            size = page.size or 0

            lines.append(f'    <Page Image="{idx}" ImageSize="{size}"{_data}/>')
        lines.append('    </Pages>')
        lines.append('</ComicInfo>')

        return '\n'.join(lines)

    def title(self, value: str):
        self.__data['title'] = value

    def series(self, value: str):
        self.__data['series'] = value

    def number(self, value: str):
        self.__data['number'] = value

    def volume(self, value: str):
        self.__data['volume'] = value

    def alternate_series(self, value: str):
        self.__data['alternate_series'] = value

    def series_group(self, value: str):
        self.__data['series_group'] = value

    def summary(self, value: str):
        self.__data['summary'] = value

    def notes(self, value: str):
        self.__data['notes'] = value

    def year(self, value: str):
        self.__data['year'] = value

    def month(self, value: str):
        self.__data['month'] = value

    def day(self, value: str):
        self.__data['day'] = value

    def writer(self, value: str):
        self.__data['writer'] = value

    def penciller(self, value: str):
        self.__data['penciller'] = value

    def inker(self, value: str):
        self.__data['inker'] = value

    def colorist(self, value: str):
        self.__data['colorist'] = value

    def letterer(self, value: str):
        self.__data['letterer'] = value

    def cover_artist(self, value: str):
        self.__data['cover_artist'] = value

    def editor(self, value: str):
        self.__data['editor'] = value

    def publisher(self, value: str):
        self.__data['publisher'] = value

    def genre(self, value: str):
        self.__data['genre'] = value

    def web(self, value: str):
        self.__data['web'] = value

    def page_count(self, value: str):
        self.__data['page_count'] = value

    def language(self, value: str):
        self.__data['language'] = value

    def iso(self, value: str):
        self.__data['iso'] = value

    def age_rating(self, value: str):
        self.__data['age_rating'] = value

    def characters(self, value: str):
        self.__data['characters'] = value

    def teams(self, value: str):
        self.__data['teams'] = value

    def scan_information(self, value: str):
        self.__data['scan_information'] = value

    def pages(self, pages: List[Page]):
        self.__pages = pages

