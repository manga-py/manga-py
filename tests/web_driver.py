import unittest

from pyvirtualdisplay import Display

from manga_py.base_classes import WebDriver


class TestWebDriver(unittest.TestCase):
    def test_driver(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = WebDriver().get_driver()
        driver.get('http://httpbin.org')
        elements = driver.find_elements_by_css_selector('a')
        count = len(elements)
        driver.close()
        display.stop()
        self.assertTrue(count > 0)
