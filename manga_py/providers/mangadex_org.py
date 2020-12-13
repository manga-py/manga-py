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

    def get_archive_name(self) -> str:
        prev = super().get_archive_name()
        code = self.chapter['lang_code']
        return '{}-{}'.format(prev, self.__countries.get(code, 'Other'))

    def get_chapter_index(self) -> str:
        return self.chapter['chapter'].replace('.', '-')

    def manga_idx(self):
        return self.re.search(r'/(?:manga|title)/(\d+)', self.get_url()).group(1)

    def get_content(self):
        if self.__content is None:
            content = self.http_get('{}/api/?id={}&type=manga'.format(self.domain, self.manga_idx()))
            self.__content = self.json.loads(content)
        return self.__content

    def get_manga_name(self) -> str:
        return self.content['manga']['title']

    @property
    def _chapters(self):
        chapters = []
        for idx in self.content['chapter']:
            ch = self.content['chapter'][idx]  # type: dict
            ch.update({
                'key': idx,
            })
            chapters.append(ch)
        return chapters

    def _quest_languages(self):
        _languages = self._languages
        arg_language = self.arg('language')
        if arg_language is None:
            languages = self.quest(
                [],
                'Available languages:\n{}\n\nPlease, select your lang (empty for all, comma for delimiter lang):'.format(
                    '\n'.join(_languages)
                )).split(',')
        else:
            languages = arg_language.split(',')

        return languages

    def get_chapters(self):
        if self.__chapters is None:
            languages = self._quest_languages()
            _ch = self.filter_chapters(self._chapters, languages)

            translator = self.arg('translator')
            if translator is not None:
                _ch = self.filter_chapters_translator(_ch, translator)

            self.__chapters = _ch

        return self.__chapters

    @property
    def _languages(self) -> list:
        if self.__languages is None:
            self.__languages = []
            self.__fill_languages()
        return self.__languages

    def __fill_languages(self):
        for lang in self._chapters:
            if lang['lang_code'] not in self.__languages:
                self.__languages.append(lang['lang_code'])

    def filter_chapters(self, chapters, languages: list) -> list:
        if len(languages) == 0 or languages[0].strip(' ') == '':
            return chapters
        return [chapter for chapter in chapters if chapter['lang_code'] in languages]

    def filter_chapters_translator(self, chapters, translator: str) -> list:
        enc_translator = escape(translator)
        return [chapter for chapter in chapters if (
                chapter['group_name'] == translator or chapter['group_name'] == enc_translator
        )]

    def get_files(self):
        content = self.json.loads(self.http_get('{}/api/?id={}&server=null&type=chapter'.format(
            self.domain,
            self.chapter['key']
        )))
        return ['{}{}/{}'.format(content['server'], content['hash'], img) for img in content['page_array']]

    def get_cover(self) -> str:
        return '{}{}'.format(
            self.domain,
            self.content['manga']['cover_url'],
        )

    def chapter_for_json(self) -> str:
        return '{}-{}'.format(self.chapter['volume'] or '0', self.chapter['chapter'])

    # region specified data for eduhoribe/comic-builder

    def chapter_details(self, chapter) -> dict:
        return {
            "chapter": chapter['chapter'],
            "volume": chapter['volume'],
            "title": chapter['title'],
            "language": chapter['lang_name'],
            "publisher": chapter['group_name']
        }

    def manga_details(self):
        if 'manga' not in self.content:
            return

        information = self.content['manga']
        manga_code = self.original_url.rsplit('/', 2)[1]
        covers = {
            MangaDexOrg.extract_cover_volume_number(cover): '{}{}'.format(self.domain, cover)
            for cover in information['covers'] if MangaDexOrg.standard_cover_url_pattern(cover, manga_code)
        }

        return {
            "title": information['title'],
            "description": information['description'],
            "authors": [author for author in {information['author'], information['artist']} if author != ''],
            "sauce": self.original_url,
            "volume_covers": covers,
        }

    @staticmethod
    def standard_cover_url_pattern(inf, manga_code):
        return re.search(r'.*{}v\d+$'.format(manga_code), inf.rsplit('.', 1)[0]) is not None

    @staticmethod
    def extract_cover_volume_number(inf):
        return inf.rsplit('.', 1)[0].rsplit('v', 1)[1]

    # endregion


main = MangaDexOrg
