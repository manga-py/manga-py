from manga_py.provider import Provider
from .helpers.std import Std


class MangaSh(Provider, Std):
    _api_url = 'https://api.manga.sh/api/v1/'
    _cdn_url = 'https://cdn.manga.sh/'
    __local_storage = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        _ch = chapter.get('ChapterNumberAbsolute', self.chapter_id)
        _vol = chapter.get('VolumeNumber', 0)
        _ch_v = chapter.get('ChapterNumberVolume', '')
        if _ch_v:
            _ch_v = '_' + _ch_v
        return '{}-{}{}'.format(_vol, _ch, _ch_v)

    def get_main_content(self):
        if not self.__local_storage:
            idx = self._get_name(r'/comics/(\d+)')
            url = '{}series_chapters?query=SeriesId.Id:{}&order=asc&sortby=TimeUploaded&limit=0&offset=0'
            content = self.http_get(url.format(self._api_url, idx))
            self.__local_storage = self.json.loads(content)
        return self.__local_storage

    def get_manga_name(self) -> str:
        content = self.content.get('response')[0]
        return content.get('SeriesId').get('Name')

    def get_chapters(self):
        return list(self.content.get('response', []))

    def get_files(self):
        chapter = self.chapter
        _hash = chapter.get('Hash')
        url = '{}series_chapters/{}'
        items = self.json.loads(self.http_get(url.format(self._api_url, _hash)))
        items = items.get('response', [{}])[0].get('SeriesChaptersFiles', {})
        return [self._cdn_url + i.get('Name') for i in items]

    def get_cover(self) -> str:
        content = self.content.get('response')[0]
        content = content.get('SeriesId').get('CoverImage')
        return '{}/covers/{}'.format(self._cdn_url, content)


main = MangaSh
