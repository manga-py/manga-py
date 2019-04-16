from .gomanga_co import GoMangaCo
from .helpers.std import Std
from time import sleep
from requests import get


class LHTranslationCom(GoMangaCo, Std):
    _name_re = r'/(?:truyen|manga)-([^/]+)\.html'
    _content_str = '{}/manga-{}.html'
    _chapters_selector = '#tab-chapper td > a.chapter,#list-chapters a.chapter'

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'-chapter-(.+?)\.html', self.chapter)
        return idx.group(1).replace('.', '-')

    def get_files(self):
        content = self.http_get(self.chapter)
        parser = self.document_fromstring(content, 'article#content,.chapter-content', 0)
        self.http()._download = self._download
        return self._images_helper(parser, 'img.chapter-img', 'data-original')

    def _download(self, file_name, url, method):
        now_try_count = 0
        while now_try_count < 10:
            with open(file_name, 'wb') as out_file:
                now_try_count += 1
                response = get(url, timeout=60, allow_redirects=True)
                if response.status_code >= 400:
                    self.http().debug and print('ERROR! Code {}\nUrl: {}'.format(
                        response.status_code,
                        url,
                    ))
                    sleep(2)
                    continue
                out_file.write(response.content)
                response.close()
                out_file.close()
                break


main = LHTranslationCom
