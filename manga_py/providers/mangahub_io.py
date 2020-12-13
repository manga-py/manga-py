from manga_py.provider import Provider
from .helpers.std import Std


class MangaHubIo(Provider, Std):
    _api = 'https://api.mghubcdn.com/graphql'
    _cdn = 'https://img.mghubcdn.com/file/imghub/'

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        return self.re.search(r'/chapter/[^/]+/\w+-([^/]+)', chapter).group(1)

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/(?:manga|chapter)/([^/]+)')

    def get_chapters(self):
        return self._elements('.list-group .list-group-item > a')

    def get_files(self):
        query = "{chapter(x:mh01,slug:\"%(name)s\",number:%(num)d)" \
                "{id,title,mangaID,number,slug,date,pages,noAd,manga" \
                "{id,title,slug,mainSlug,author,isWebtoon,isYaoi,isPorn,isSoftPorn,unauthFile,isLicensed" \
                "}}}" % {'name': self.manga_name, 'num': self.chapter_id + 1}
        content = self.json.loads(self.http_post(self._api, data={
            "query": query
        }))

        pages = content.get('data', {}).get('chapter', {}).get('pages', '{}')
        pages = self.json.loads(pages)

        images = []
        for p in pages:
            images.append('{}{}'.format(self._cdn, pages[p]))
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('.row > div > img.img-responsive')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaHubIo
