#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest


class TestGhPages(unittest.TestCase):
    def test_make(self):
        from helpers.gh_pages import main
        main()
