#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from os import path

from manga_py.providers import providers_list

root_path = path.dirname(path.realpath(__file__))


class TestProvidersUnique(unittest.TestCase):
    def test_unique(self):
        providers = []
        for k in providers_list:
            for p in providers_list[k]:
                self.assertFalse(p in providers, 'Duplicate reg {}'.format(p))
                providers.append(p)


