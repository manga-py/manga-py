#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from os import path
from shutil import copyfile

from manga_py import fs
from manga_py.base_classes import Archive

root_path = path.dirname(path.realpath(__file__))

files_paths = [
    ['/files/img1.jpg', '/temp/img1.jpg'],
    ['/files/img2.png', '/temp/img2.png'],
    ['/files/img3.jpg', '/temp/img3.jpg'],
    ['/files/img4.jpg', '/temp/img4.jpg'],
    ['/files/img5.png', '/temp/img5.png'],
    ['/files/img6.gif', '/temp/img6.gif'],
    ['/files/img7.webp', '/temp/img7.webp'],
]


class TestArchive(unittest.TestCase):

    def test_make_archive(self):
        arc = Archive()
        arc_path = root_path + '/temp/arc.zip'
        fs.unlink(arc_path)
        orig_size = 0
        for idx, item in enumerate(files_paths):
            fs.unlink(root_path + item[1])
            copyfile(root_path + item[0], root_path + item[1])
            orig_size += int(fs.file_size(root_path + item[1]))
            arc.add_file(root_path + item[1])

        copyfile(root_path + '/files/archive_test_file', root_path + '/temp/archive_test_file')
        orig_size += int(fs.file_size(root_path + '/temp/archive_test_file'))
        arc.add_file(root_path + '/temp/archive_test_file')

        copyfile(root_path + '/files/archive_test_image', root_path + '/temp/archive_test_image')
        orig_size += int(fs.file_size(root_path + '/temp/archive_test_image'))
        arc.add_file(root_path + '/temp/archive_test_image')

        arc.make(arc_path)
        size = fs.file_size(arc_path)
        self.assertTrue(size and 1024 < int(size) < orig_size)
