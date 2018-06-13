from manga_py.provider import Provider
from .helpers.std import Std


class VizCom(Provider, Std):

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.chapter_id)

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        url = self.re.search('/([^/]+/chapters/[^/]+)').group(1)
        return self.http_get('{}/{}'.format(self.domain, url))

    def get_manga_name(self) -> str:
        return self._get_name('/chapters/([^/]+)')

    def get_chapters(self):
        return self._elements('.o_products .chapter-text > a')

    def get_files(self):
        volume_id = self.re.search('/chapter/[^/]+/(\d+)', self.chapter)
        params = [
            'device%5Fid=3',
            # 'page={}',
            'manga%5Fid={}'.format(volume_id.groups()[0]),
            'loadermax=1',
        ]

        uri = '{}/manga/get_manga_url?'.format(self.domain)
        uri += '&'.join(params)

        n = 0
        _img_index = 0
        while n < 299:  # FIXME!

            _img_index += 1
            page_url = '{}&page={}'.format(uri, n)

            parser = self.html_fromstring(page_url, 'ImageLoader')

            if not len(parser):
                break

            # TODO!
            # t = MultiThreads()
            #
            # for i in parser:
            #     img_url = i.get('url')
            #     if ~img_url.find('blankpage.jpg'):
            #         break
            #     # see manga.py:280
            #     t.addThread(download_one_file, (img_url,))
            #     # safe_downloader(img_url, path.join(temp_root_path, 'img_{:0>3}.jpg'.format(_img_index)))
            # t.startAll()

            n += 2

        return [-1]

    def get_cover(self):
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass


main = VizCom
