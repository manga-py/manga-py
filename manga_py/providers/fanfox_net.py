from manga_py.provider import Provider
from .helpers.std import Std


class MangaFoxMe(Provider, Std):

    def get_archive_name(self) -> str:
        groups = self._ch_parser()
        ch = groups[1].replace('.', '-')
        vol = ['0']
        if groups[0]:
            vol = [groups[0]]
        return self.normal_arc_name({'vol': vol, 'ch': ch})

    def _ch_parser(self):
        selector = r'/manga/[^/]+/(?:v([^/]+)/)?c([^/]+)/'
        groups = self.re.search(selector, self.chapter).groups()
        return groups

    def get_chapter_index(self) -> str:
        """
        examples:
        <domain>/manga/<name>/v03/c020/1.html
        <domain>/manga/<name>/v03/c020.5/1.html
        <domain>/manga/<name>/v01/c019/1.html
        <domain>/manga/<name>/c022/1.html
        <domain>/manga/<name>/c021/1.html
        <domain>/manga/<name>/v04/c016.5/1.html
        <domain>/manga/<name>/v18/c154.5/1.html
        <domain>/manga/<name>/vTBD/c169/1.html
        <domain>/manga/<name>/v06/c018.5/1.html]
        <domain>/manga/<name>/v03/c020.5/1.html
        <domain>/manga/<name>/v08/c031/1.html
        """
        groups = self._ch_parser()
        idx = groups[1].replace('.', '-')
        if not ~idx.find('-'):
            idx = idx + '-0'
        if groups[0]:
            return '{}-{}'.format(idx, groups[0])
        return idx

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)/?')

    def get_chapters(self):
        return self._elements('#chapters a.tips')

    def __get_files_url(self):
        volume = self.chapter
        url = self.http().normalize_uri(volume)
        if ~url.find('.html'):
            url = url[: url.rfind('/')]
        return url

    def get_files(self):
        img_selector = 'img#image'
        _url = self.__get_files_url()
        url = '{}/1.html'.format(_url)
        selector = '#top_bar .r .l select.m'
        parser = self.html_fromstring(url)
        images = self._images_helper(parser, img_selector)
        for page in self._first_select_options(parser, selector, True):
            n = page.get('value')
            if int(n) < 2:  # first / comments page
                continue
            url = '{}/{}.html'.format(_url, n)
            parser = self.html_fromstring(url)
            images += self._images_helper(parser, img_selector)
        return images

    def get_cover(self):
        pass  # TODO

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaFoxMe
