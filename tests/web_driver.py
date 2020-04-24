import unittest

from selenium.common.exceptions import TimeoutException

from manga_py.base_classes.web_driver import make_driver, get_display


class TestWebDriver(unittest.TestCase):
    def test_driver(self):
        driver = make_driver()
        self.assertIsNotNone(driver)
        driver.get('https://ya.ru')
        result = True
        try:
            driver.find_element('#text,.logo-wrapper')
        except TimeoutException:
            result = False
        driver().close()
        get_display() is None or get_display().stop()
        self.assertTrue(result)
