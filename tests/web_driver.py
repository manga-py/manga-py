import unittest

from selenium.common.exceptions import TimeoutException

from manga_py.base_classes.web_driver import get_driver, display


class TestWebDriver(unittest.TestCase):
    def test_driver(self):
        driver = get_driver()
        self.assertIsNotNone(driver)
        driver.get('https://ya.ru')
        result = True
        try:
            driver.find_element('#text,.logo-wrapper')
        except TimeoutException:
            result = False
        driver.close()
        display is None or display.stop()
        self.assertTrue(result)
