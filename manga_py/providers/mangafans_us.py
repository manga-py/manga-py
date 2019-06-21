from .manganelo_com import MangaNeloCom


class MangaFansUs(MangaNeloCom):
    chapter_re = r'[/-]chap(?:ter)?[_-](\d+(?:\.\d+)?(?:-v\d)?)'

    def get_chapter(self):
        return '%s/0' % self.chapter

    def get_manga_name(self) -> str:
        _ = self.re.search(r'(/(?:read-)?manga/)([^/]+)', self.get_url())
        self._prefix = _.group(1)
        return _.group(2)


main = MangaFansUs
