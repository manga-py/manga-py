from libs.provider import Provider


class MangaGoMe(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        type = self.re.search('/(mf|raw)', self.get_current_chapter()).group(1)
        return 'vol_{:0>3}-{}-{}'.format(*idx, type)

    def get_chapter_index(self) -> str:
        selector = '/(?:mf|raw)/.*?(\\d+)(?:\\.(\\d+))?'
        chapter = self.get_current_chapter()
        groups = self.re.search(selector, chapter).groups()
        idx = [
            groups[0],
            0 if len(groups) < 2 else groups[1],
        ]
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        url = '{}/read-manga/{}/'.format(self.get_domain(), self.get_manga_name())
        return self.html_fromstring(url, '#information', 0)

    def get_manga_name(self) -> str:
        return self.re.search('/read\\-manga/([^/]+)/', self.get_url()).group(1)

    def get_chapters(self):
        content = self.storage_main_content()
        chapters = content.cssselect('#chapter_table a.chico')
        raws = content.cssselect('#raws_table a.chico')
        return [i.get('href') for i in chapters + raws]

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        parser = self.re.search("imgsrcs.+[^.]+?var.+?=\\s?'(.+)'", content)
        if not parser:
            return []
        return parser.group(0).split(',')

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaGoMe
