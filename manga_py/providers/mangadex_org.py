from manga_py.provider import Provider
from .helpers.std import Std


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
        return '{}-{}'.format(prev, self.__countries[code])

    def get_chapter_index(self) -> str:
        return self.chapter['chapter'].replace('.', '-')

    def manga_idx(self):
        return self.re.search(r'/(?:manga|title)/(\d+)', self.get_url()).group(1)

    def get_main_content(self):
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

    def get_chapters(self):
        if self.__chapters is None:
            languages = self.quest(
                [],
                'Available languages:\n{}\n\nPlease, select your lang (empty for all, space for delimiter lang):'.format(
                    '\n'.join(self._languages)
                )).split(' ')
            self.__chapters = self.filter_chapters(languages)
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

    def filter_chapters(self, languages: list) -> list:
        if len(languages) == 0 or languages[0].strip(' ') == '':
            return self._chapters
        return [chapter for chapter in self._chapters if chapter['lang_code'] in languages]

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


main = MangaDexOrg
