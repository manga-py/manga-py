from os import chmod
from sys import platform
from zipfile import ZipFile

from requests import get

from manga_py.fs import is_file, dirname, storage, path_join, get_util_home_path


class WebDriver:
    driver_version = '2.40'

    @staticmethod
    def is_win():
        return ~platform.find('win32')

    def download_drivder(self):
        url_prefix = 'https://chromedriver.storage.googleapis.com/'
        url = '/chromedriver_linux64.zip'
        if ~platform.find('darwin'):
            url = '/chromedriver_mac64.zip'
        if self.is_win():
            url = '/chromedriver_win32.zip'

        path = path_join(get_util_home_path(), 'driver.zip')

        with open(path, 'wb') as driver:
            driver.write(get(url_prefix + self.driver_version + url).content)
            driver.close()
        with ZipFile(path) as file:
            file.extractall(dirname(self._driver_path()))

    def _driver_path(self):
        if self.is_win():
            driver = 'chromedriver.exe'
        else:
            driver = 'chromedriver'
        return path_join(get_util_home_path(), driver)

    def get_driver(self):
        from selenium import webdriver  # need, if captcha detected
        driver_path = self._driver_path()
        if not is_file(driver_path):
            self.download_drivder()
        self.is_win() or chmod(driver_path, 0o755)
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.set_window_size(500, 600)
        return driver
