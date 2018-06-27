#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from os import path

from manga_py.libs import fs
from tests import *

root_path = path.join(path.dirname(path.realpath(__file__)), 'tests')


if __name__ == '__main__':
    fs.make_dirs(root_path + '/temp')
    unittest.main()
