import json
from os import chmod
from pathlib import Path
from re import compile
from tarfile import open as tar_open
from zipfile import ZipFile

from requests import get
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from .web_driver import WebDriver, _is_win, _is_mac, _is_linux, UnsupportedOsException


class FirefoxDriver(WebDriver):
    url_api = 'https://api.github.com/repos/mozilla/geckodriver/releases'
    url_driver = 'https://github.com/mozilla/geckodriver/releases/download/{ver}/{arc}'
    _arc = 'geckodriver-{ver}-{os}.{ext}'

    def __init__(self, version: str = None):
        super().__init__(('v%s' % (version or '0.26.0').lstrip('v')), compile(r'(.+)/'))

    def driver_archive(self) -> str:
        if _is_linux():
            return self._arc.format(ver=self.driver_version, os='linux64', ext='tar.gz')
        if _is_mac():
            return self._arc.format(ver=self.driver_version, os='macos', ext='tar.gz')
        if _is_win():
            return self._arc.format(ver=self.driver_version, os='win64', ext='zip')
        raise UnsupportedOsException()

    def driver_path(self) -> Path:
        _driver = 'geckodriver'
        if _is_win():
            _driver += '.exe'
        return self.home_path.joinpath(_driver)

    def download_driver(self) -> None:
        driver = 'driver'
        if _is_win():
            driver += '.zip'
        else:
            driver += '.tgz'
        path = str(self.home_path.joinpath(driver))

        with open(path, 'wb') as _driver:
            _driver.write(get(self.url_driver.format(
                ver=self.driver_version,
                arc=self.driver_archive()
            )).content)
            _driver.close()
        if _is_win():
            with ZipFile(path) as file:
                _path = str(self.driver_path().parent)
                file.extractall(_path)
        else:
            _path = str(self.driver_path().parent)
            tar_open(path).extractall(_path)

    def _make_driver(self) -> None:
        _path = self.driver_path()
        driver_path = str(_path)
        if not _path.is_file():
            self.download_driver()
        _is_win() or chmod(driver_path, 0o755)
        options = Options()
        options.set_preference("media.volume_scale", "0.0")
        options.headless = not self.visible
        self._driver = Firefox(
            executable_path=driver_path,
            options=options,
        )

    def get_available_versions(self) -> set:
        content = json.loads(get(self.url_api).text)
        return {i['tag_name'][1:] for i in content if 'master' == i['target_commitish']}


__all__ = ['FirefoxDriver']
