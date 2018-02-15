from src.providers.gomanga_co import GoMangaCo


class NoraNoFansubCom(GoMangaCo):
    _name_re = r'\.com/(?:lector/)?(?:series/|read/)?([^/]+)/'
    _content_str = '{}/{}/'
    _chapters_selector = '.entry-content td a[href]'

    def _get_json_selector(self, content):
        return r'var\spages\s*=\s*(\[.+\])'

    def get_chapters(self):
        return super().get_chapters()[::-1]

    def prepare_cookies(self):
        pass

    def get_cover(self) -> str:
        return self._cover_from_content('.entry-content img.size-full')


main = NoraNoFansubCom
