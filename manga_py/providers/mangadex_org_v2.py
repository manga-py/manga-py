import time
import typing

from manga_py.provider import Provider
from .helpers.std import Std


class MangaDexOrg(Provider, Std):
    api_url = 'https://api.mangadex.org'

    # https://mangadex.org/title/80422e14-b9ad-4fda-970f-de370d5fa4e5/made-in-abyss

    __chapters = None
    __languages = None
    _selected_languages = []
    __countries = {
        '': 'Other',
        'bd': 'Bengali',
        'bg': 'Bulgarian',
        'br': 'Portuguese (Br)',
        'cn': 'Chinese (Simp)',
        'ct': 'Catalan',
        'cz': 'Czech',
        'de': 'German',
        'dk': 'Danish',
        'es': 'Spanish (Es)',
        'fi': 'Finnish',
        'fr': 'French',
        'gb': 'English',
        'gr': 'Greek',
        'hk': 'Chinese (Trad)',
        'hu': 'Hungarian',
        'id': 'Indonesian',
        'il': 'Hebrew',
        'in': 'Hindi',
        'ir': 'Persian',
        'it': 'Italian',
        'jp': 'Japanese',
        'kr': 'Korean',
        'lt': 'Lithuanian',
        'mm': 'Burmese',
        'mn': 'Mongolian',
        'mx': 'Spanish (LATAM)',
        'my': 'Malay',
        'nl': 'Dutch',
        'no': 'Norwegian',
        'ph': 'Filipino',
        'pl': 'Polish',
        'pt': 'Portuguese (Pt)',
        'ro': 'Romanian',
        'rs': 'Serbo-Croatian',
        'ru': 'Russian',
        'sa': 'Arabic',
        'se': 'Swedish',
        'th': 'Thai',
        'tr': 'Turkish',
        'ua': 'Ukrainian',
        'vn': 'Vietnamese',
    }

    def _get(self, part, method='get') -> dict:
        response = self.http().requests(f'{self.api_url}/{part}', method=method)
        if response.status_code >= 400:
            self.log(f'Bad status code {response.status_code}')
            raise RuntimeError(f'Bad status code {response.status_code}')
        data = response.json()
        if data['result'] != 'ok':
            raise RuntimeError('Bad result: \n' + '\n'.join([err['detail'] for err in data['errors']]))
        return data

    def get_archive_name(self) -> str:
        prev = super().get_archive_name()
        code = self.chapter['attributes']['translatedLanguage']

        translator = self._translators(self.chapter)
        translator_name = ''
        if len(translator) == 1:
            translator_name = translator[0] + '-'

        return '{}-{}{}'.format(prev, translator_name, self.__countries.get(code, 'Other'))

    def get_chapter_index(self) -> str:
        return '{}-{}'.format((self.volume_num(self.chapter) or ''), self.chapter_num(self.chapter)).strip('-')

    def manga_idx(self):
        return self.re.search(r'/title/([^/]+)', self.get_url()).group(1)

    def get_content(self):
        return self._get(
            f'manga/{self.manga_idx()}?includes[]=artist&includes[]=author&includes[]=cover_art'
        ).get('data', {})

    def get_manga_name(self) -> str:
        titles = self.content['attributes']['title']
        if len(self._available_languages) > 1:
            self._selected_languages = self._quest_languages()

        for lng in titles:
            return titles[lng]
        return self.manga_idx()

    def get_chapters(self):
        _ch = self._chapters(self._selected_languages)

        if len(self._languages) > 1:
            _ch = self.filter_chapters(_ch, self._selected_languages)

        translator = self.arg('translator')
        if translator is not None:
            _ch = self.filter_chapters_translator(_ch, translator)

        return _ch

    def get_files(self):
        data = self._get(f'at-home/server/{self.chapter["id"]}?forcePort443=false')
        base_url = data['baseUrl']
        hash_ = data['chapter']['hash']
        return [f'{base_url}/data/{hash_}/{img}' for img in data['chapter']['data']]

    def get_cover(self) -> typing.Optional[str]:
        relationships = self.content['relationships']
        for attribute in relationships:
            if attribute['type'] == 'cover_art':
                filename = attribute['attributes']['fileName']
                return f'https://uploads.mangadex.org/covers/{self.manga_idx()}/{filename}'
        return None

    def chapter_for_json(self) -> str:
        return '{}-{}'.format(self.volume_num(self.chapter) or '0', self.chapter_num(self.chapter))

    def _chapters(self, languages: typing.Optional[typing.List[str]] = None):
        if self.__chapters is None:
            self.__chapters = []
            limit = 96
            offset = 0
            while True:
                self.log(f'Get chapters with offset {offset}')
                url = f'manga/{self.manga_idx()}/feed?limit={limit}&includes[]=scanlation_group&includes[]=' \
                      f'user&order[volume]=desc&order[chapter]=desc&offset={offset}&contentRating[]=' \
                      f'safe&contentRating[]=suggestive&contentRating[]=erotica&contentRating[]=pornographic'
                if languages is not None:
                    url += ('&' + '&'.join([f'&translatedLanguage[]={lng}' for lng in languages]))
                content = self._get(url)
                self.__chapters += content['data']
                if content['total'] < content['offset'] + limit:
                    break
                offset = content['offset']
                time.sleep(1)
        return self.__chapters

    def _quest_languages(self):
        arg_language = self.arg('language')
        if arg_language is None:
            languages = self.quest(
                [],
                'Available languages:\n{}\n\n'
                'Please, select your lang (empty for all, comma for delimiter lang):'.format(
                    '\n'.join(self._languages)
                ))
        else:
            languages = arg_language

        return list(set([lng.strip() for lng in languages.split(',')]))

    @property
    def _available_languages(self):
        return self.content['attributes']['availableTranslatedLanguages']

    @property
    def _languages(self) -> list:
        if self.__languages is None:
            self.__languages = self._available_languages
        return self.__languages

    @staticmethod
    def filter_chapters(chapters, languages: list) -> list:
        if len(languages) == 0 or languages[0] == '':
            return chapters
        return [chapter for chapter in chapters if chapter['attributes']['translatedLanguage'] in languages]

    def filter_chapters_translator(self, chapters, translator: str) -> list:
        return [chapter for chapter in chapters if len(set(self._translators(chapter)) & {translator.lower()}) > 0]

    def _translators_data(self, chapter):
        return [r for r in chapter['relationships'] if r['type'] == 'scanlation_group']

    def _translators(self, chapter):
        return [r['attributes']['name'].lower() for r in self._translators_data(chapter)]

    @staticmethod
    def chapter_num(chapter):
        return chapter['attributes']['chapter']

    @staticmethod
    def volume_num(chapter):
        return chapter['attributes']['volume']

    def prepare_cookies(self):
        self._params['max_threads'] = 2

    # region specified data for eduhoribe/comic-builder

    def chapter_details(self, chapter) -> dict:
        attributes = chapter['attributes']
        return {
            'chapter': self.chapter_num(chapter),
            'volume': self.volume_num(chapter),
            'title': attributes['title'],
            'language': attributes['translatedLanguage'],
            'publisher': 'See "publishers"',
            'publishers': self._translators(chapter),
        }

    def manga_details(self):
        def get_from_relationship(type_: str) -> list:
            relationships = self.content['relationships']
            return [relationship for relationship in relationships if relationship['type'] == type_]

        authors = [r['attributes']['name'] for r in get_from_relationship('author')]
        artists = [r['attributes']['name'] for r in get_from_relationship('artist')]
        return {
            'id': self.manga_idx(),
            'title': self.manga_name,
            'description': 'See "descriptions"',
            'descriptions': self.content['attributes']['description'],
            'authors': [author for author in {*authors, *artists} if author != ''],
            'sauce': self.original_url,
            'covers': {'main': self.get_cover()}
        }
    # endregion


main = MangaDexOrg
