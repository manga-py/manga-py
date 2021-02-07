import re
from manga_py.provider import Provider
from .helpers.std import Std
from html import escape


class MangaDexOrg(Provider, Std):
    __content = None
    __chapters = None
    __languages = None
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

    def _get(self, part):
        return self.http().requests('{}/api/v2/{}'.format(
            self.domain,
            part.format(self.manga_idx())),
        ).json()

    def get_archive_name(self) -> str:
        prev = super().get_archive_name()
        code = self.chapter['language']
        return '{}-{}'.format(prev, self.__countries.get(code, 'Other'))

    def get_chapter_index(self) -> str:
        return self.chapter['chapter'].replace('.', '-')

    def manga_idx(self):
        return self.re.search(r'/(?:manga|title)/(\d+)', self.get_url()).group(1)

    def get_content(self):
        return 'nope'

    def get_manga_name(self) -> str:
        self.__content = self._get('manga/{}').get('data', {})
        return self.__content.get('title')

    def get_chapters(self):
        _ch = self._chapters

        if len(self._languages) > 1:
            languages = self._quest_languages()

            _ch = self.filter_chapters(_ch, languages)

        translator = self.arg('translator')
        if translator is not None:
            _ch = self.filter_chapters_translator(_ch, translator)

        return _ch

    def get_files(self):
        content = self._get(f'chapter/{self.chapter["hash"]}').get('data', {})
        server = content['server']
        _hash = content['hash']
        return [f'{server}{_hash}/{img}' for img in content['pages']]

    def get_cover(self) -> str:
        return self.content['mainCover']

    def chapter_for_json(self) -> str:
        return '{}-{}'.format(self.chapter['volume'] or '0', self.chapter['chapter'])

    @property
    def _chapters(self):
        if self.__chapters is None:
            self.__chapters = self._get('manga/{}/chapters').get('data', {})
        return self.__chapters.get('chapters', [])

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

        return list([lng.strip() for lng in languages.split(',')])

    @property
    def _languages(self) -> list:
        if self.__languages is None:
            self.__languages = list(set([ch['language'] for ch in self._chapters]))
        return self.__languages

    def filter_chapters(self, chapters, languages: list) -> list:
        if len(languages) == 0 or languages[0] == '':
            return chapters
        return [chapter for chapter in chapters if chapter['language'] in languages]

    def filter_chapters_translator(self, chapters, translator: str) -> list:
        enc_translator = escape(translator)
        return [chapter for chapter in chapters if len(set(self._translators(chapter)) & {enc_translator}) > 0]

    def _translators(self, chapter):
        groups = self.__chapters.get('groups', [])
        return [g['name'] for g in groups if g['id'] in chapter['groups']]

    # region specified data for eduhoribe/comic-builder

    def chapter_details(self, chapter) -> dict:
        return {
            'chapter': chapter['chapter'],
            'volume': chapter['volume'],
            'title': chapter['title'],
            'language': chapter['language'],
            'publisher': 'See "publishers"',
            'publishers': self._translators(chapter)
        }

    @staticmethod
    def _flat_array(arg):
        if arg is None:
            return ['']
        if type(arg) == list:
            return arg
        if type(arg) == str:
            return [arg]
        raise TypeError('Unknown type!')

    def manga_details(self):
        author = self._flat_array(self.__content.get('author', ''))
        artist = self._flat_array(self.__content.get('artist', ''))
        return {
            'id': self.manga_idx(),
            'title': self.__content['title'],
            'description': self.__content['description'],
            'authors': [author for author in {*author, *artist} if author != ''],
            'sauce': self.original_url,
            'covers': {'main': self.__content.get('mainCover')}
        }
    # endregion


main = MangaDexOrg
