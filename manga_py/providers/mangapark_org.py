from manga_py.provider import Provider
from .helpers.std import Std


class MangaParkOrg(Provider, Std):
    __url = None

    def get_chapter_index(self) -> str:
        return self.chapter[0].replace('.', '-')

    def get_main_content(self):
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

    def get_chapters(self):
        # multi-lang!
        variants = self._elements('div.card')
        answer = '1'
        if len(variants) > 1:
            self._print_variants(variants)
            answer = self._answer(len(variants))
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


main = MangaParkOrg
