from ..provider import Provider
from .helpers.std import Std
from manga_py.base_classes.web_driver import make_driver
from manga_py.base_classes.web_driver.web_driver import WebDriver
from time import sleep


class JapScanCom(Provider, Std):
    _chapters_selector = '#chapters_list .chapters_list a'
    driver = None

    def get_chapter_index(self) -> str:
        return self.re.search(r'.+/(\d+(?:\.\d+)?)/', self.chapter).group(1).replace('.', '-')

    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga/([^/]+)')

    def get_chapters(self) -> list:
        chapters = self._elements(self._chapters_selector)
        n = self.http().normalize_uri
        return [n(i.get('href')) for i in chapters]

    def get_files(self):
        content = self.http_get(self.chapter)
        pages = self.document_fromstring(content, 'select#pages option')
        n = self.http().normalize_uri
        return [n(i.get('value')) for i in pages]

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        _path, idx, _url = self._save_file_params_helper(url, idx)
        self.driver.get(url)
        image = self._images()

        self.after_file_save(_path, idx)
        self._archive.add_file(_path)

        callable(callback) and callback()

        return _path

    def prepare_cookies(self):
        raise RuntimeError('Provider not worked')

        self._params['max_threads'] = 1
        self.driver = make_driver('chrome')

    def _image(self):
        image = self.driver.find_element('#image')
        sleep(5)
        shadow = self.driver.find_element('cnv-vv')
        canvases_len = self.driver.driver.execute_script('return arguments[0].all_canvas.length;', shadow)
        canvases = []
        for i in range(int(canvases_len)):
            canvases.append(self.driver.driver.execute_script(
                'return arguments[0].all_canvas[arguments[1]].toDataURL("image/png").substring(21);',
                shadow, i
            ))
        return None


main = JapScanCom
