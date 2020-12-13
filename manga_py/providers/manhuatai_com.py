from random import randrange

from manga_py.provider import Provider
from .helpers.std import Std


class ManhuaTaiCom(Provider, Std):
    servers = [
        'http://mhpic.mh51.com',
        'http://mhpic.manhualang.com',
        'http://mhpic.jumanhua.com',
        'http://mhpic.yyhao.com',
    ]

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return self.normal_arc_name({'vol': [
            self.chapter_id, idx
        ]})

    def get_chapter_index(self) -> str:
        ch = self.chapter
        return self.re.search(r'/([^/]+)\.html', ch).group(1)

    def get_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)')

    def get_chapters(self):
        topics = self._elements('[id^=topic]')
        items = []
        for i in topics[::-1]:
            items += i.cssselect('a')
        return items

    @staticmethod
    def _decode_img_path(page_id, img_path):
        result = ''
        pid = int(page_id) % 10
        for i in img_path:
            result += chr(ord(i) - pid)
        return result

    def get_server(self):
        idx = randrange(0, len(self.servers))
        return self.servers[idx]

    def get_files(self):
        content = self.http_get(self.chapter)
        pageid = self.re.search(r'pageid:\s*(\d+)', content).group(1)
        imgpath = self.re.search(r'imgpath:\s*[\'"](.+?)[\'"]', content).group(1)
        startimg = self.re.search(r'startimg:\s*(\d+)', content).group(1)
        totalimg = self.re.search(r'totalimg:\s*(\d+)', content).group(1)
        comic_size = self.re.search(r'comic_size:\s*[\'"](.+?)[\'"]', content).group(1)

        imgpath = self._decode_img_path(pageid, imgpath)

        items = []
        for i in range(int(startimg), int(totalimg) + 1):
            items.append('{}/comic/{}{}.jpg{}'.format(
                self.get_server(),
                imgpath,
                i,
                comic_size
            ))
        return items

    def get_cover(self) -> str:
        return self._cover_from_content('.comic-cover > img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ManhuaTaiCom
