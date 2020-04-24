from abc import ABCMeta, abstractmethod
from pathlib import Path
from sys import platform

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as BrowserDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located as locate,
    presence_of_element_located as locate_one
)
from selenium.webdriver.support.ui import WebDriverWait
from typing import List
from time import sleep

from manga_py.fs import get_util_home_path

class UnsupportedOsException(Exception):
    def __init__(self, os=platform, *args, **kwargs):
        super().__init__(os, *args, **kwargs)


def _is_win():
    return platform.startswith('win32') or platform.startswith('cygwin')


def _is_mac():
    return platform.startswith('darwin')


def _is_linux():
    return platform.startswith('linux')


def _supported() -> bool:
    return _is_win() or _is_mac() or _is_linux()


class WebDriver(metaclass=ABCMeta):
    driver_version = None
    home_path = None
    _re = None
    _driver = None
    _default_timeout = 10
    __visible = True
    __freq = 1.0

    def __init__(self, version: str, _re):
        self.driver_version = version
        self._re = _re
        self.home_path = Path(get_util_home_path())

    @property
    def visible(self) -> bool:
        return self.__visible

    @visible.setter
    def visible(self, visible: bool):
        self.__visible = visible

    @staticmethod
    @abstractmethod
    def driver_archive() -> str:
        raise NotImplementedError

    @abstractmethod
    def driver_path(self) -> Path:
        raise NotImplementedError

    @abstractmethod
    def download_driver(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _make_driver(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_available_versions(self) -> set:
        raise NotImplementedError

    def _version(self, version: str) -> str:
        return self._re.search(version).group(1)

    @property
    def initialized(self) -> bool:
        return self._driver is not None

    def init_driver(self):
        if not self.initialized:
            self._make_driver()
        return self

    @property
    def freq(self) -> float:
        return float(self.__freq)

    @freq.setter
    def freq(self, freq: float):
        self.__freq = freq

    @property
    def driver(self) -> BrowserDriver:
        if not self.initialized:
            self.init_driver()
        return self._driver

    def get(self, url):
        self.driver.get(url)

    @property
    def valid_url(self):
        if self.initialized:
            url = self._driver.current_url
            if url and url.startswith('http'):
                return True
        return False

    @property
    def _wait(self):
        return WebDriverWait(self._driver, self._default_timeout, poll_frequency=self.freq)

    def find_element(self, selector: str, by=By.CSS_SELECTOR) -> List[WebElement]:
        sleep(1)
        return self._wait.until(locate_one((by, selector)))

    def find_all_elements(self, selector: str, by=By.CSS_SELECTOR) -> List[WebElement]:
        sleep(1)
        self._wait.until(locate_one((by, selector)))  # wait for first element
        sleep(1)
        return self._wait.until(locate((by, selector)))

    def add_cookie(self, key, value, **kwargs):
        _cookie = {
            'name': key,
            'value': value,
            'expiry': 1898789118,
            'secure': False,
            'path': '/',
            'httpOnly': False,
        }

        _cookie.update(kwargs)

        self._driver.add_cookie(_cookie)

    def close(self):
        if self.initialized:
            self._driver.quit()


__all__ = ['WebDriver', '_is_win', '_is_mac', '_is_linux', '_supported', 'UnsupportedOsException']
