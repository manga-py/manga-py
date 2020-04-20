#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from os import path, name as os_name
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

        copyfile(root_path + '/files/archive_test_image', root_path + '/temp/archive_test_image')
        orig_size += int(fs.file_size(root_path + '/temp/archive_test_image'))
        arc.add_file(root_path + '/temp/archive_test_image')

        arc.make(arc_path)
        size = fs.file_size(arc_path)
        self.assertTrue(size and 1024 < int(size) < orig_size)

    def test_rename(self):
        copyfile(root_path + '/files/archive_test_file', root_path + '/temp/archive_test_file')
        fs.rename(root_path + '/temp/archive_test_file', root_path + '/temp/archive_test_file1')
        self.assertTrue(fs.is_file(root_path + '/temp/archive_test_file1'))
        self.assertFalse(fs.is_file(root_path + '/temp/archive_test_file'))

    def test_home(self):
        if os_name != 'nt':
            self.assertTrue(fs.get_util_home_path().find('/home/') == 0)
        self.assertTrue(fs.is_dir(fs.get_util_home_path()))

    def test_unlink1(self):
        _dir = fs.get_util_home_path()
        fs.make_dirs(_dir + '/dir')
        self.assertRaises(OSError, fs.unlink, _dir)

    def test_unlink2(self):
        _dir = fs.get_util_home_path()
        fs.make_dirs(_dir + '/dir')
        fs.unlink(_dir, True)
        self.assertFalse(fs.is_dir(_dir))

    def test_not_filesize(self):
        self.assertIsNone(fs.file_size(fs.get_util_home_path() + '/file'))

    def test_check_free_space1(self):
        self.assertTrue(fs.check_free_space(fs.get_util_home_path(), min_size=99))

    def test_check_free_space2(self):
        self.assertFalse(fs.check_free_space(fs.get_util_home_path(), 99, True))
