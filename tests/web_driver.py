import unittest

from pyvirtualdisplay import Display
from selenium.common.exceptions import NoSuchElementException

from manga_py.base_classes import WebDriver


class TestWebDriver(unittest.TestCase):
    def test_driver(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = WebDriver().get_driver()
        driver.get('https://ya.ru')
        result = True
        try:
            driver.find_element_by_id('text')
        except NoSuchElementException:
            result = False
        driver.close()
        display.stop()
        self.assertTrue(result)
