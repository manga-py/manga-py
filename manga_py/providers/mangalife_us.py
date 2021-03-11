from manga_py.provider import Provider
from .helpers.std import Std


class MangaLifeUs(Provider, Std):
    img_selector = '.image-container .CurImage'

    def get_chapter_index(self) -> str:
        selector = r'-chapter-(\d+)-index-(\d+)'
        chapter = self.re.search(selector, self.chapter)

        if chapter is None:  # http://mangalife.us/manga/Ubau-Mono-Ubawareru-Mono  #51
            selector = r'-chapter-(\d+(?:\.\d+)?)'
            chapter = self.re.search(selector, self.chapter).group(1).split('.')
            return '-'.join(chapter)

        chapter = chapter.groups()

        return '{}-{}'.format(
            chapter[0],
            1 if chapter[1] is None else chapter[1],
        )

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        uri = self.get_url()
        test = self.re.search(r'\.\w{2,7}/read-online/', uri)
        if test:
            uri = self.html_fromstring(uri, 'a.list-link', 0).get('href')
        return self.re.search(r'(?:\.\w{2,7})?/manga/([^/]+)', uri).group(1)

    def _chapters_js(self):
        raw_chapters = self.re.search(r'vm.Chapters\s*=\s*(\[\{.+\}\])', self.content).group(1)
        chapters = self.json.loads(raw_chapters)

        return ['{}/read-online/{}-chapter-{}-index-{}.html'.format(
            self.domain,
            self.manga_name,
            self.__ch(ch['Chapter']),
            ch['Chapter'][0],  # example mangasee123.com/manga/Tower-Of-God
        ) for ch in chapters]

    def _chapters_html(self):
        return self._elements('.list a.list-group-item')

    def get_chapters(self):
        try:
            return self._chapters_js()
        except:
            return self._chapters_html()

    def _files_js(self, content):
        re_domain = self.re.search(r'ng-src="https://\{\{(.+?)}}', content).group(1)
        domain = self.re.search(fr"""{re_domain}\s*=\s*["'](.+)['"]""", content).group(1)
        raw_chapter = self.json.loads(self.re.search(r"""vm.CurChapter\s*=\s*(\{.+\})""", content).group(1))

        chapter = raw_chapter['Chapter']
        directory = raw_chapter['Directory']
        pages = int(raw_chapter['Page'])

        if len(directory) > 0:
            directory += '/'

        return ['https://{}/manga/{}/{}{}-{}.png'.format(
            domain,
            self.manga_name,
            directory,
            self.__one_ch(chapter),
            '{:0>3}'.format(i)
        ) for i in range(1, pages + 1)]

    def _files_html(self, content):
        parser = self.document_fromstring(content)
        return self._images_helper(parser, '.image-container-manga > .fullchapimage > img')

    def get_files(self):
        _chapter = self.chapter
        try:
            _chapter = self.re.search(r'(.+)-page-\d+\.html', _chapter).group(1)
        except AttributeError:
            pass

        content = self.http_get('%s.html' % _chapter)

        try:
            return self._files_js(content)
        except:
            return self._files_html(content)

    @staticmethod
    def __one_ch(ch):
        chapter = ch[1:-1]
        if ch[-1] == '0':
            return chapter
        return '%s.%s' % (chapter, ch[-1])

    @staticmethod
    def __ch(ch):
        n = ch[1:-1].lstrip('0')
        if ch[-1] != '0':
            return '%s.%s' % (n, ch[-1])
        return '{:0>1}'.format(n)

    def prepare_cookies(self):
        self.http().cookies['FullPage'] = 'yes'

    def get_cover(self) -> str:
        return self._cover_from_content('.leftImage img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaLifeUs
