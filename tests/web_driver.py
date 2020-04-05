import unittest

from selenium.common.exceptions import TimeoutException

from manga_py.base_classes.web_driver import get_driver


class TestWebDriver(unittest.TestCase):
    def test_driver(self):
        driver = get_driver()
        driver.get('https://ya.ru')
        result = True
        try:
            driver.find_element('#text')
        except TimeoutException:
            result = False
        driver.close()
        self.assertTrue(result)
