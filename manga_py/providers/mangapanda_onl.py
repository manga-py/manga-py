from manga_py.provider import Provider
from .helpers.std import Std


class MangaPandaCom(Provider, Std):
    _cdn = 'https://img.mghubcdn.com/file/imghub'
    _api_url = 'https://api.mghubcdn.com/graphql'

    def get_chapter_index(self) -> str:
        return self.chapter_for_json()

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/manga/([^/]+)')

    def get_chapters(self):
        # curl 'https://api.mghubcdn.com/graphql' -H 'Content-Type: application/json' --data-raw '{"query": "{latestPopular(x:mr02){id}manga(x:mr02,slug:\"mahou-tsukai-no-yome\"){id,rank,title,slug,status,image,latestChapter,author,artist,genres,description,alternativeTitle,mainSlug,isYaoi,isPorn,isSoftPorn,unauthFile,noCoverAd,isLicensed,createdDate,updatedDate,chapters{id,number,title,slug,date}}}"}'

        keys = [
            'id', 'rank', 'title', 'slug', 'status', 'chapters'
        ]

        data = self._api(
            r'{manga(x:mr02,slug:"%(name)s"){%(keys)s{id,number,title,slug,date}}}'
            % {'name': self.manga_name, 'keys': ','.join(keys)}
        )

        chapters = data.get('data', {}).get('manga', {}).get('chapters', [])  # type: list

        return chapters[::-1]

    def get_files(self):
        data = self._api(
            r'{chapter(x:mr02,slug:"%(name)s",number:%(number)f){id,title,mangaID,number,slug,date,pages}}'
            % {'name': self.manga_name, 'number': self.chapter['number']}
        )

        images = data.get('data', {}).get('chapter', {}).get('pages', [])

        if type(images) == str:
            images = self.json.loads(images)  # type: list

        return list(map(lambda x: '{}/{}'.format(self._cdn, images[x]), images))

    def get_cover(self):
        return self._cover_from_content('.manga-thumb')

    def chapter_for_json(self) -> str:
        number = str(self.chapter['number']).replace('.', '-')
        slug = self.chapter['slug']

        return '{}_{}'.format(number, slug)

    def _api(self, query: str) -> dict:
        response = self.http().requests(self._api_url, method='post', data={
            "query": query,
        }, headers={
            'Accept': 'application/json',
        })

        return response.json()


main = MangaPandaCom
