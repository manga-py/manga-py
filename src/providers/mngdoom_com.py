from src.provider import Provider


class MngDoomCom(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        groups = self.re_search('\\.com?/[^/]+/(\\d+)(?:\\.(\\d+))').groups()
        idx = [
            groups[0],
            0 if len(groups) < 2 else groups[1]
        ]
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re_search('\\.co/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        items = self.document_fromstring(self.get_storage_content(), 'ul.chapter-list > li > a')
        return [i.get('href') for i in items]

    def prepare_cookies(self):
        pass

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        items = self.re_search(' images = (\\[{[^;]+}\\])', content)
        if not items:
            return []
        try:
            images = self.json.loads(items.group(1))
            return [i['url'] for i in images]
        except self.json.JSONDecodeError:
            return []

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MngDoomCom
