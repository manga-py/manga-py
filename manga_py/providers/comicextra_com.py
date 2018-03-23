from manga_py.provider import Provider
from .helpers.std import Std


class ComicExtra(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self._storage['current_chapter'])

    def get_chapter_index(self) -> str:
        return self._storage['current_chapter']
        # return self.re.search('(\d+)', self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/comic/{}')

    def get_manga_name(self):
        url = self.get_url()
        test = self.re.search('/comic/([^/]+)', url)
        if test:
            return test.group(1)
        return self.re.search('/([^/]+)/chapter', url).group(1)

    def get_chapters(self):
        return self.document_fromstring(self.content, '#list td a')

    def get_files(self):
        url = self.chapter + '/full'
        items = self.html_fromstring(url, '.chapter-container img.chapter_img')
        return [i.get('src') for i in items]

    def get_cover(self):
        return self._cover_from_content('.movie-image img')


main = ComicExtra
