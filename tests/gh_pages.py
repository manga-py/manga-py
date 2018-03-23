#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from os import path


class TestGhPages(unittest.TestCase):
    def test_make(self):
        from helpers.gh_pages import main
        main()
