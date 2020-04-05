from os import chmod
from pathlib import Path
from re import compile
from zipfile import ZipFile

from lxml import etree
from requests import get
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from .web_driver import WebDriver, _is_win, _is_mac, _is_linux, UnsupportedOsException


class ChromeDriver(WebDriver):
    url_prefix = 'https://chromedriver.storage.googleapis.com'

    def __init__(self, version: str = None):
        super().__init__((version or '79.0.3945.36'), compile(r'(.+)/'))

    @staticmethod
    def driver_archive() -> str:
        if _is_linux():
            return 'chromedriver_linux64.zip'
        if _is_mac():
            return 'chromedriver_mac64.zip'
        if _is_win():
            return 'chromedriver_win32.zip'
        raise UnsupportedOsException()

    def driver_path(self) -> Path:
        _driver = 'chromedriver'
        if _is_win():
            _driver += '.exe'
        return self.home_path.joinpath(_driver)

    def download_driver(self) -> None:
        path = str(self.home_path.joinpath('driver.zip'))

        with open(path, 'wb') as _driver:
            _driver.write(get('{prefix}/{version}/{driver}'.format(
                prefix=self.url_prefix,
                version=self.driver_version,
                driver=self.driver_archive()
            )).content)
            _driver.close()
        with ZipFile(path) as file:
            _path = str(self.driver_path().parent)
            file.extractall(_path)

    def _make_driver(self) -> None:
        _path = self.driver_path()
        driver_path = str(_path)
        if not _path.is_file():
            self.download_driver()
        _is_win() or chmod(driver_path, 0o755)
        options = Options()
        options.add_argument("--mute-audio")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.headless = not self.visible

        self._driver = Chrome(
            executable_path=driver_path,
            options=options,
        )

    def get_available_versions(self) -> set:
        response = get(self.url_prefix)
        xml = etree.fromstring(response.content)
        versions = []
        for child in xml.getchildren():  # type: etree._Element
            for child_child in child.getchildren():  # type: etree._Element
                tag = child_child.tag
                text = child_child.text
                if ~tag.find('Key') and ~text.find('.zip'):
                    versions.append(self._version(text))
        return set(versions)


__all__ = ['ChromeDriver']
