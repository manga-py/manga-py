#!/usr/bin/python3
# -*- coding: utf-8 -*-


<<<<<<< HEAD
import unittest
from os import path, mkdir, listdir
import shutil
from PIL import Image
from sys import path as sys_path
__dirname__ = path.dirname(path.realpath(__file__))
sys_path.append(path.realpath(path.join(__dirname__, '..')))
import manga
from helpers import remove_void as cropper
from helpers import exceptions


class Arguments:
    def setArgument(self, name, value):
        setattr(self, name, value)

    def setArguments(self, arguments):
        for name, value in arguments:
            self.setArgument(name, value)


class TestCase(unittest.TestCase):
    def setUp(self):
        self.current_id = ''
        self.root_path = __dirname__
        self.path = path.join(self.root_path, 'temp')
        self.arguments = Arguments()
        self.arguments.setArguments([  # default arguments
            # ('url', None),
            ('name', 'Manga'),
            ('destination', self.path),
            ('info', False),
            ('progress', False),
            ('skip_volumes', 0),
            ('user_agent', ''),
            ('no_name', False),
            ('allow_webp', False),
            ('reverse_downloading', False),
            ('rewrite_exists_archives', False),
            ('xt', 0),
            ('xr', 0),
            ('xb', 0),
            ('xl', 0),
            ('crop_blank', False),
            ('crop_blank_factor', 100),
            ('crop_blank_max_size', 30),
            ('max_volumes', 1),
            ('multi_threads', False),
            ('no_multi_threads', False),
            ('force_png', False)
        ])

    def _prepare_arguments(self):
        setattr(manga, 'info_mode', self.arguments.info)
        setattr(manga, 'show_progress', self.arguments.progress)
        setattr(manga, 'add_name', not self.arguments.no_name)
        setattr(manga, 'name', self.arguments.name)
        if len(self.arguments.user_agent):
            setattr(manga, 'user_agent', self.arguments.user_agent)

        setattr(manga, 'add_name', not self.arguments.no_name)
        setattr(manga, 'arguments', self.arguments)

    def _before_test(self):
        if path.isdir(self.path):
            shutil.rmtree(self.path)
        mkdir(self.path)

    def __test_url(self, url):
        self.arguments.setArgument('url', url)
        self._prepare_arguments()
        downloader = manga.MangaDownloader(url, self.arguments.name)

        downloader.main()

        _files = [name for name in listdir(path.join(self.path, 'Manga'))]
        count_files = len(_files)
        return count_files > 0

    def test_error_url(self):
        url = 'http://example.org/manga'
        self.arguments.setArgument('url', url)
        self._prepare_arguments()
        result = False
        try:
            manga.MangaDownloader(url, self.arguments.name)
        except exceptions.ProviderNotFound:
            result = True
        self.assertTrue(result)


    # def _urls_true(self, urls):
    #     self._before_test()
    #     for url in urls:
    #         self.assertTrue(self.__test_url(url))

    def _urls_false(self, urls):
        self._before_test()
        for url in urls:
            try:
                result = True
                self.__test_url(url)
            except exceptions.VolumesNotFound:
                result = False
            self.assertFalse(result)

    def _prepare_cropper(self, need_copy=True, source_file='img1.jpg', tested_file=None):
        self._before_test()

        if not tested_file:
            tested_file = source_file

        source_file = path.join(self.root_path, source_file)
        tested_file = path.join(self.path, tested_file)

        if need_copy:
            shutil.copyfile(source_file, tested_file)

        self.cropper = cropper.Cropper()

        return source_file, tested_file

    def test_cropper_left(self):
        source_file, tested_file = self._prepare_cropper(True)

        self.cropper.set_sourced_file(tested_file)
        self.cropper.crop({'left': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size
        self.assertTrue((source_sizes[0] - tested_sizes[0]) == 10)

    def test_cropper_right(self):
        source_file, tested_file = self._prepare_cropper(True)

        self.cropper.set_sourced_file(tested_file)
        self.cropper.crop({'right': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size
        self.assertTrue((source_sizes[0] - tested_sizes[0]) == 10)

    def test_cropper_top(self):
        source_file, tested_file = self._prepare_cropper(True)

        self.cropper.set_sourced_file(tested_file)
        self.cropper.crop({'top': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size
        self.assertTrue((source_sizes[1] - tested_sizes[1]) == 10)

    def test_cropper_bottom(self):
        source_file, tested_file = self._prepare_cropper(True)

        self.cropper.set_sourced_file(tested_file)
        self.cropper.crop({'bottom': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size
        self.assertTrue((source_sizes[1] - tested_sizes[1]) == 10)

    def test_cropper_autocrop_default(self):
        self._before_test()
        source_file, tested_file = self._prepare_cropper(False, 'img1.jpg')

        self.cropper.set_sourced_file(source_file)
        self.cropper.process(tested_file)

        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size

        self.assertTrue(source_sizes[0] > tested_sizes[0])
        self.assertTrue(source_sizes[1] > tested_sizes[1])

    def test_cropper_autocrop_1(self):
        self._before_test()
        source_file, tested_file = self._prepare_cropper(False, 'img1.jpg')

        epsilon = self.cropper.epsilon
        self.cropper.set_epsilon(0)
        self.cropper.set_sourced_file(source_file)
        self.cropper.process(tested_file, 1, 1)
        self.cropper.set_epsilon(epsilon)

        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size

        self.assertTrue(source_sizes[0] == tested_sizes[0])
        self.assertTrue(source_sizes[1] - 1 == tested_sizes[1])

    def test_cropper_autocrop_0(self):
        self._before_test()
        source_file, tested_file = self._prepare_cropper(False, 'img1.jpg')

        self.cropper.set_sourced_file(source_file)
        self.cropper.process(tested_file, 1, 0)

        self.assertFalse(path.isfile(tested_file))

    def test_cropper_no_blanks(self):
        self._before_test()
        source_file, tested_file = self._prepare_cropper(False, 'img2.png')

        self.cropper.set_sourced_file(source_file)
        self.assertFalse(self.cropper.process(tested_file))

    def test_cropper_no_blanks1(self):
        self._before_test()
        source_file, tested_file = self._prepare_cropper(False, 'img3.jpg')

        self.cropper.set_sourced_file(source_file)
        self.assertFalse(self.cropper.process(tested_file, 254))  # don't allow crop gray

    def test_cropper_no_blanks2(self):
        self._before_test()
        source_file, tested_file = self._prepare_cropper(False, 'img3.jpg')

        self.cropper.set_sourced_file(source_file)
        self.cropper.process(tested_file, 2)  # allow crop gray

        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size

        self.assertTrue(source_sizes[0] > tested_sizes[0])
        self.assertTrue(source_sizes[1] > tested_sizes[1])

    def test_cropper_no_blanks3(self):
        self._before_test()
        source_file, tested_file = self._prepare_cropper(False, 'img4.jpg')

        self.cropper.set_sourced_file(source_file)
        self.cropper.process(tested_file, 2)  # allow crop gray

        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size

        self.assertTrue(source_sizes[0] > tested_sizes[0])
        self.assertTrue(source_sizes[1] > tested_sizes[1])

    def test_png(self):
        self._before_test()
        source_file, tested_file = self._prepare_cropper()
        dest = cropper.ImageFormat.convert(tested_file)
        self.assertTrue(path.isfile(dest))
        pass


=======
>>>>>>> origin/dev_0.3
if __name__ == '__main__':
    # unittest.main()
    pass
