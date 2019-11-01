from manga_py.provider import Provider
from .helpers.std import Std


class MangaDexOrg(Provider, Std):
    __content = None
    __chapters = None

    def get_archive_name(self) -> str:
        return self.normal_arc_name({
            'vol': self.chapter['volume'],
            'ch': self.chapter['chapter'],
        })

    def get_chapter_index(self) -> str:
        return self.chapter_for_json()

    def manga_idx(self):
        return self.re.search(r'/manga/(\d+)', self.get_url()).group(1)

    def get_main_content(self):
        if self.__content is None:
            content = self.http_get('https://mangadex.org/api/?id={}&type=manga'.format(self.manga_idx()))
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
                    '\n'.join(self.languages())
                )).split(' ')
            self.__chapters = self.filter_chapters(languages)
        return self.__chapters

    def languages(self) -> list:
        languages = []
        for lang in self._chapters:
            if lang['lang_code'] not in languages:
                languages.append(lang['lang_code'])
        return languages

    def filter_chapters(self, languages: list) -> list:
        if len(languages) == 0 or languages[0] == '':
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
        return '{}-{}'.format(self.chapter['volume'], self.chapter['chapter'])


main = MangaDexOrg
