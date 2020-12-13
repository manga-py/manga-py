from manga_py.provider import Provider
from .helpers.std import Std


class MangaParkOrg(Provider, Std):
    __url = None

    def get_chapter_index(self) -> str:
        return self.chapter[0].replace('.', '-')

    def get_content(self):
        return self.http_get(self.__url)

    def get_manga_name(self) -> str:
        title = self.html_fromstring(self.get_url(), 'h3 > a, h4 > a', 0)
        self.__url = self.http().normalize_uri(title.get('href'))
        return title.text_content().strip()

    def _print_variants(self, variants):
        self.log('Please, select lang. (empty for all langs)')
        for n, i in enumerate(variants):
            lng = i.cssselect('.card-header a')[0].text_content()
            self.log('\n%d: ' % (n + 1) + lng, end='')

    def _answer(self, max_digit):
        while True:
            answer = self.quest([], 'Answer (digit): ')
            if len(answer) > 0 and (int(answer) > max_digit or int(answer) <= 0):
                self.log('Wrong answer! Try one more.')
            else:
                return answer

    def _auto_language(self, variants):
        language = self.arg('language')

        if language is not None:

            for n, variant in enumerate(variants):
                text = variant.cssselect('.flag + a.ml-1')[0].text_content()  # type: str

                if ~text.find('[' + language + ']'):
                    return n + 1

        return None

    def _auto_translator(self, variants):
        translator = self.arg('translator')

        if translator is not None:

            for n, variant in enumerate(variants):
                text = variant.cssselect('.flag + a.ml-1')[0].text_content()  # type: str

                lng = text.find(']')
                if ~text.find(translator, lng):
                    return n + 1

        return None

    def _auto_rules(self, variants, default):
        auto_lang = self._auto_language(variants)
        auto_translator = self._auto_translator(variants)

        if auto_lang is not None:
            return auto_lang

        if auto_translator is not None:
            return auto_translator

        if len(variants) > 1:
            self._print_variants(variants)
            return self._answer(len(variants))

        return default

    def get_chapters(self):
        # multi-lang!
        variants = self._elements('div.card')
        answer = self._auto_rules(variants, '1')

        if len(variants) > 1 and not len(answer):
            parser = self.document_fromstring(self.content)
        else:
            parser = variants[int(answer) - 1]

        items = parser.cssselect('.card-body i + a')
        result = []
        re = self.re.compile(r'[Cc]h\.(\d+(?:\.\d+)?)')
        n = self.http().normalize_uri
        for i in items:
            text = i.text_content()
            result.append((
                re.search(text).group(1),
                n(i.get('href')),
            ))
        return result

    def get_files(self):
        re = self.re.compile(r'images\s*=\s*(\[.+\]);')
        content = self.http_get(self.chapter[1])
        items = self.json.loads(re.search(content).group(1))
        return items

    def get_cover(self) -> str:
        return self._cover_from_content('.order-0 > img')

    def book_meta(self) -> dict:
        pass

    def chapter_for_json(self) -> str:
        return self.chapter[1]

    def prepare_cookies(self):
        self.http().cookies['set'] = 'theme=1&h=1&img_load=4&img_zoom=5&img_tool=4&twin_m=0&twin_c=0&manga_a_warn=1&history=1&timezone=14'


main = MangaParkOrg
