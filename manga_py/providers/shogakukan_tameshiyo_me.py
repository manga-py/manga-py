from manga_py.crypt import BaseLib
from manga_py.provider import Provider
from .helpers.std import Std


class ShogakukanTameshiyoMe(Provider, Std):
    __local_storage = None
    _site = 'https://shogakukan.tameshiyo.me'
    img_url = '/imgDeliver?gcode='

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_content(self):
        pass

    def get_manga_name(self) -> str:
        return self._get_name('/(\d+)')

    def get_chapters(self):
        return [b'']

    def before_file_save(self, url, idx):
        _url = self._site + self.img_url + self.__local_storage['code']
        _url = self.http_post(_url, data={
            'base64': '1',
            'vsid': self.__local_storage['vsid'],
            'trgCode': url,
        }, headers={'Referer': self._site})
        return _url

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        if url is None:
            _url = self.get_current_file()
        else:
            _url = url

        _path, idx, _url = self._save_file_params_helper(_url, idx)
        _path += '.jpg'

        with open(_path, 'wb') as file:
            file.write(BaseLib.base64decode(_url))

        callable(callback) and callback()
        self.after_file_save(_path, idx)
        self._archive.add_file(_path, in_arc_name)

        return _path

    @property
    def chapter_url(self):
        url = self.chapter
        if isinstance(url, bytes):
            url = self.get_url()
        return url

    def get_files(self):
        parser = self.html_fromstring(self.chapter_url)
        self.__local_storage = {
            'vsid': parser.cssselect('input[data-key="vsid"]')[0].get('value'),
            'code': parser.cssselect('input[data-key="isbn1kan"]')[0].get('value'),
        }
        return [i.get('value') for i in parser.cssselect('input[data-key="imageCodes"]')]

    def get_cover(self) -> str:
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.get_url()


main = ShogakukanTameshiyoMe
