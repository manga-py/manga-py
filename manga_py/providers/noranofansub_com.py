from .gomanga_co import GoMangaCo


class NoraNoFansubCom(GoMangaCo):
    _name_re = r'\.\w{2,7}/(?:lector/)?(?:series/|read/)?([^/]+)/'
    _content_str = '{}/{}/'
    _chapters_selector = '.entry-content td a[href]'

    def get_chapters(self):
        return super().get_chapters()[::-1]

    def get_cover(self) -> str:
        return self._cover_from_content('.entry-content img.size-full')


main = NoraNoFansubCom
