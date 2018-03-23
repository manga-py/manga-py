#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from os import path

from pyvirtualdisplay import Display

from manga_raw.base_classes import WebDriver


class TestWebDriver(unittest.TestCase):
    def test_driver(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = WebDriver().get_driver()
        driver.get('http://httpbin.org')
        elements = driver.find_elements_by_css_selector('#manpage ul > li > a')
        count = len(elements)
        driver.close()
        display.stop()
        self.assertTrue(count > 0)
