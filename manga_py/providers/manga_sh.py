from manga_py.provider import Provider
from .helpers.std import Std


class MangaSh(Provider, Std):
    _api_url = 'https://api.manga.sh/api/v1/'
    _cdn_url = 'https://cdn.manga.sh/'

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        _ch = chapter.get('ChapterNumberAbsolute', self.chapter_id)
        _vol = chapter.get('VolumeNumber', 0)
        _ch_v = chapter.get('ChapterNumberVolume', '')
        if _ch_v:
            _ch_v = '_' + _ch_v
        return '{}-{}{}'.format(_vol, _ch, _ch_v)

    def get_main_content(self):
        idx = self._get_name(r'/comics/(\d+)')
        url = '{}series_chapters?query=SeriesId.Id:{}&order=asc&sortby=TimeUploaded&limit=0&offset=0'
        content = self.http_get(url.format(self._api_url, idx))
        return self.json.loads(content)

    def get_manga_name(self) -> str:
        content = self.content.get('response')[0]
        return content.get('SeriesId').get('Name')

    def get_chapters(self):
        return list(self.content.get('response', []))

    def _url_helper(self, chapter):
        return '{}series_chapters/{}'.format(
            self._api_url,
            chapter.get('Hash')
        )

    def get_files(self):
        url = self._url_helper(self.chapter)
        items = self.json.loads(self.http_get(url))
        items = items.get('response', [{}])[0].get('SeriesChaptersFiles', {})
        return [self._cdn_url + i.get('Name') for i in items]

    def get_cover(self) -> str:
        content = self.content.get('response')[0]
        content = content.get('SeriesId').get('CoverImage')
        return '{}/covers/{}'.format(self._cdn_url, content)

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self._url_helper(self.chapter)


main = MangaSh
