from src.provider import Provider


class ZingBoxMe(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}'.format(idx)

    def get_chapter_index(self) -> str:
        return str(self.get_current_chapter().get('title', ''))

    def get_main_content(self):
        idx = self.re.search('/manga/(?:[^/]+/)?(\d+)/', self.get_url())
        _ = {
            'url': '/manga/getBookDetail/{}'.format(idx.group(1)),
            'method': 'GET',
            'api': '/mangaheatapi/web',
        }
        return self.http_post(self.get_domain() + '/api', data=_)

    def get_manga_name(self) -> str:
        return self.re.search('\\.me/manga/(?:\\d+/)?([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        try:
            return self.json.loads(self.get_storage_content()).get('child', [])
        except self.json.JSONDecodeError:
            return []

    def prepare_cookies(self):
        pass

    def get_files(self):
        idx = self.get_current_chapter().get('chapterId', 0)
        _ = {
            'url': '/manga/getChapterImages/{}'.format(idx),
            'method': 'GET',
            'api': '/mangaheatapi/web',
        }
        images = self.http_post(self.get_domain() + '/api', data=_)
        return self.json.loads(images).get('images', [])

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = ZingBoxMe
