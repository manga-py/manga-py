#!/usr/bin/python3
# -*- coding: utf-8 -*-


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
        self.assertTrue(downloader.status)

        downloader.process()

        _files = [name for name in listdir(path.join(self.path, 'Manga'))]
        count_files = len(_files)
        return count_files > 0

    def test_error_url(self):
        url = 'http://example.org/manga'
        self.arguments.setArgument('url', url)
        self._prepare_arguments()
        downloader = manga.MangaDownloader(url, self.arguments.name)
        self.assertFalse(downloader.status)

    def _urls_true(self, urls):
        self._before_test()
        for url in urls:
            self.assertTrue(self.__test_url(url))

    def _urls_false(self, urls):
        self._before_test()
        for url in urls:
            try:
                result = True
                self.__test_url(url)
            except exceptions.VolumesNotFound:
                result = False
            self.assertFalse(result)

    def _prepare_cropper(self, need_copy=True, img_name='img1.jpg'):
        self._before_test()
        source_file = path.join(self.root_path, img_name)
        tested_file = path.join(self.path, img_name)

        if need_copy:
            shutil.copyfile(source_file, tested_file)

        return source_file, tested_file

    def test_cropper_left(self):
        source_file, tested_file = self._prepare_cropper()

        cropper.crop(tested_file, {'left': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size
        self.assertTrue((source_sizes[0] - tested_sizes[0]) == 10)

    def test_cropper_right(self):
        source_file, tested_file = self._prepare_cropper()

        shutil.copyfile(source_file, tested_file)
        cropper.crop(tested_file, {'right': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size
        self.assertTrue((source_sizes[0] - tested_sizes[0]) == 10)

    def test_cropper_top(self):
        source_file, tested_file = self._prepare_cropper()

        cropper.crop(tested_file, {'top': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size
        self.assertTrue((source_sizes[1] - tested_sizes[1]) == 10)

    def test_cropper_bottom(self):
        source_file, tested_file = self._prepare_cropper()

        shutil.copyfile(source_file, tested_file)
        cropper.crop(tested_file, {'bottom': 10})
        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size
        self.assertTrue((source_sizes[1] - tested_sizes[1]) == 10)

    def test_cropper_autocrop_default(self):
        self._before_test()
        source_file = path.join(self.root_path, 'img1.jpg')
        tested_file = path.join(self.path, 'img1.jpg')

        cropper.process(source_file, tested_file)

        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size

        self.assertTrue(source_sizes[0] > tested_sizes[0])
        self.assertTrue(source_sizes[1] > tested_sizes[1])

    def test_cropper_autocrop_1(self):
        self._before_test()
        source_file = path.join(self.root_path, 'img1.jpg')
        tested_file = path.join(self.path, 'img1.jpg')

        cropper.process(source_file, tested_file, 1, 1)

        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size

        self.assertTrue(source_sizes[0] == tested_sizes[0])
        self.assertTrue(source_sizes[1] - 1 == tested_sizes[1])

    def test_cropper_autocrop_0(self):
        self._before_test()
        source_file = path.join(self.root_path, 'img1.jpg')
        tested_file = path.join(self.path, 'img1.jpg')

        cropper.process(source_file, tested_file, 1, 0)

        self.assertFalse(path.isfile(tested_file))

    def test_cropper_no_blanks(self):
        self._before_test()
        source_file = path.join(self.root_path, 'img2.png')
        tested_file = path.join(self.path, 'img2.png')

        cropper.process(source_file, tested_file)

        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size

        self.assertTrue(source_sizes[0] == tested_sizes[0])
        self.assertTrue(source_sizes[1] == tested_sizes[1])

    def test_cropper_no_blanks1(self):
        self._before_test()
        source_file = path.join(self.root_path, 'img3.jpg')
        tested_file = path.join(self.path, 'img3.jpg')

        cropper.process(source_file, tested_file, 250)  # don't allow crop gray

        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size

        self.assertTrue(source_sizes[0] == tested_sizes[0])
        self.assertTrue(source_sizes[1] == tested_sizes[1])

    def test_cropper_no_blanks2(self):
        self._before_test()
        source_file = path.join(self.root_path, 'img3.jpg')
        tested_file = path.join(self.path, 'img3.jpg')

        cropper.process(source_file, tested_file, 2)  # allow crop gray

        source_image = Image.open(source_file)
        tested_image = Image.open(tested_file)
        source_sizes = source_image.size
        tested_sizes = tested_image.size

        self.assertTrue(source_sizes[0] > tested_sizes[0])
        self.assertTrue(source_sizes[1] > tested_sizes[1])

    def test_bato_to_true(self):
        self._urls_true([
                'https://bato.to/comic/_/comics/karakai-jouzu-no-takagi-san-r13108',
            ])

    def test_bato_to_false(self):
        self._urls_false([
                'https://bato.to/comic/omics/mousou-telepathy-r0',
            ])

    def test_manga_online_biz_true(self):
        self._urls_true([
                'https://manga-online.biz/blood_bank.html'
            ])

    def test_manga_online_biz_false(self):
        self._urls_false([
                'https://manga-online.biz/False-name-manga.html'
            ])

    # def test_bato_to(self):
    #     urls = {
    #         'success': [
    #             'https://bato.to/comic/_/comics/karakai-jouzu-no-takagi-san-r13108',
    #         ],
    #         'error': [
    #             'https://bato.to/comic/omics/mousou-telepathy-r0',
    #         ],
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_balumanga_com(self):
    #     urls = {
    #         'success': [  # Site bad! There may be errors
    #             'http://bulumanga.com/mangaView.html?id=1&cid=34701&page=1&source=mangareader',
    #         ],
    #         'error': [
    #             'http://bulumanga.com/introduce.html?id=0&source=mangareader',
    #         ],
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_com_x_life(self):
    #     urls = {
    #         'success': [
    #             'https://com-x.life/4156-teenage-mutant-ninja-turtles-universe.html',
    #         ],
    #         'error': [
    #             'https://com-x.life/0-none.html',
    #         ],
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_desu_me(self):
    #     urls = {
    #         'success': [
    #             'http://desu.me/manga/horimiya.369/',
    #         ],
    #         'error': [
    #             'http://desu.me/manga/horimiya.0/',
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_funmanga_com(self):
    #     urls = {
    #         'success': [
    #             'http://www.funmanga.com/Koi-to-Uso/',
    #         ],
    #         'error': [
    #             'http://www.funmanga.com/False-name-manga',
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_gogomanga_co(self):
    #     urls = {
    #         'success': [
    #             'https://gogomanga.co/manga/in-bura.html',
    #         ],
    #         'error': [
    #             'http://www.funmanga.com/False-name-manga',
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_goodmanga_net(self):
    #     urls = {
    #         'success': [
    #             'http://goodmanga.net/16315/hakwonmul',
    #         ],
    #         'error': [
    #             'http://goodmanga.net/0',
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_heymanga_me(self):
    #     urls = {
    #         'success': [
    #             'https://www.heymanga.me/manga/Minamotokun_Monogatari',
    #         ],
    #         'error': [
    #             'https://www.heymanga.me/manga/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_inmanga_me(self):
    #     urls = {
    #         'success': [
    #             'http://inmanga.com/ver/manga/Boku-no-Hero-Academia/dda0c17a-83da-4ef6-8c65-4763e8fbe436',
    #         ],
    #         'error': [
    #             'https://www.heymanga.me/manga/False-name-manga',
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_jurnalu_ru(self):
    #     urls = {
    #         'success': [
    #             'http://inmanga.com/ver/manga/Boku-no-Hero-Academia/dda0c17a-83da-4ef6-8c65-4763e8fbe436',
    #         ],
    #         'error': [
    #             'https://www.heymanga.me/manga/False-name-manga',
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_kissmanga_com(self):
    #     urls = {
    #         'success': [
    #             'http://kissmanga.com/Manga/Kami-sama-Drop',
    #         ],
    #         'error': [
    #             'http://kissmanga.com/Manga/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_manga_online_biz(self):
    #     urls = {
    #         'success': [
    #             'https://manga-online.biz/blood_bank.html'
    #         ],
    #         'error': [
    #             'https://manga-online.biz/False-name-manga.html'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_manga_online_com_ua(self):
    #     urls = {
    #         'success': [
    #             'https://manga-online.com.ua/cmanga/378-7-kiss-7-potseluev.html'
    #         ],
    #         'error': [
    #             'https://manga-online.com.ua/cmanga/0-False-name-manga.html'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangabb_co(self):
    #     urls = {
    #         'success': [
    #             'http://www.mangabb.co/manga/2001-5'
    #         ],
    #         'error': [
    #             'http://www.mangabb.co/manga/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangabox_me(self):
    #     urls = {
    #         'success': [
    #             'https://www.mangabox.me/reader/54371/'
    #         ],
    #         'error': [
    #             'https://www.mangabox.me/reader/0/',
    #             'https://www.mangabox.me/reader/54371'  # without slash
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangachan_me(self):
    #     urls = {
    #         'success': [
    #             'http://mangachan.me/manga/46475-shin5-kekkonshite-mo-koishiteru.html'
    #         ],
    #         'error': [
    #             'http://mangachan.me/manga/1-shin5-kekkonshite-mo-koishiteru.html'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangaclub_ru(self):
    #     urls = {
    #         'success': [
    #             'https://mangaclub.ru/1201-darling-only-you-dont-know.html'
    #         ],
    #         'error': [
    #             'https://mangaclub.ru/1-darling-only-you-dont-know.html'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangaeden_com(self):
    #     urls = {
    #         'success': [
    #             'http://www.mangaeden.com/en/en-manga/yuragi-sou-no-yuuna-san/'
    #         ],
    #         'error': [
    #             'http://www.mangaeden.com/en/en-manga/yuragi-sou-no-yuuna/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangafox_me(self):
    #     urls = {
    #         'success': [
    #             'http://mangafox.me/manga/the_closer/'
    #         ],
    #         'error': [
    #             'http://mangafox.me/manga/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangafreak_net(self):
    #     urls = {
    #         'success': [
    #             'http://www3.mangafreak.net/Manga/Overlord'
    #         ],
    #         'error': [
    #             'http://www3.mangafreak.net/Manga/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangago_me(self):
    #     urls = {
    #         'success': [
    #             'http://www.mangago.me/read-manga/kimimachi_terminal/'
    #         ],
    #         'error': [
    #             'http://www.mangago.me/read-manga/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # # def test_mangahead_me(self):  # error 502 now
    # #     urls = {
    # #         'success': [
    # #             'http://mangahead.me/Manga-Raw-Scan/Fairy-Tail/'
    # #         ],
    # #         'error': [
    # #             'http://mangahead.me/Manga-Raw-Scan/False-name-manga/'
    # #         ]
    # #     }
    # #     self._urls_true(urls['success'])
    # #     self._urls_false(urls['error'])
    # 
    # def test_mangahere_co(self):
    #     urls = {
    #         'success': [
    #             'http://www.mangahere.co/manga/koi_to_uso/'
    #         ],
    #         'error': [
    #             'http://www.mangahere.co/manga/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangahome_com(self):
    #     urls = {
    #         'success': [
    #             'http://www.mangahome.com/manga/trinity_blood'
    #         ],
    #         'error': [
    #             'http://www.mangahome.com/manga/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangahub_ru(self):
    #     urls = {
    #         'success': [
    #             'https://mangahub.ru/dogma'
    #         ],
    #         'error': [
    #             'https://mangahub.ru/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangainn_net(self):
    #     urls = {
    #         'success': [
    #             'https://www.mangainn.net/manga/2944_denma'
    #         ],
    #         'error': [
    #             'https://www.mangainn.net/manga/0_denma'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangakakalot_com(self):
    #     urls = {
    #         'success': [
    #             'http://mangakakalot.com/manga/koi_to_uso'
    #         ],
    #         'error': [
    #             'http://mangakakalot.com/manga/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangaleader_com(self):
    #     urls = {
    #         'success': [
    #             'http://mangaleader.com/read-tokyo-ghoul-re/1'
    #         ],
    #         'error': [
    #             'http://mangaleader.com/read-tokyo-ghoul-re/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangalib_me(self):
    #     urls = {
    #         'success': [
    #             'https://mangalib.me/prison-school'
    #         ],
    #         'error': [
    #             'https://mangalib.me/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # # def test_mangamove_com(self):  # 502 error now
    # #     urls = {
    # #         'success': [
    # #             'http://www.mangamove.com/manga/The_Gamer/'
    # #         ],
    # #         'error': [
    # #             'http://www.mangamove.com/manga/False-name-manga/'
    # #         ]
    # #     }
    # #     self._urls_true(urls['success'])
    # #     self._urls_false(urls['error'])
    # 
    # def test_manganel_com(self):
    #     urls = {
    #         'success': [
    #             'http://manganel.com/manga/chiyoko_chocolat'
    #         ],
    #         'error': [
    #             'http://manganel.com/manga/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangaonlinehere_com(self):
    #     urls = {
    #         'success': [
    #             'http://mangaonlinehere.com/manga-info/black-or-white-sachimo'
    #         ],
    #         'error': [
    #             'http://mangaonlinehere.com/manga-info/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangapanda_com(self):
    #     urls = {
    #         'success': [
    #             'http://www.mangareader.net/akuma-no-riddle'
    #         ],
    #         'error': [
    #             'http://www.mangareader.net/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangapark_me(self):
    #     urls = {
    #         'success': [
    #             'http://mangapark.me/manga/kindaichi-shounen-no-jikenbo-20th-shuunen-kinen-series'
    #         ],
    #         'error': [
    #             'http://mangapark.me/manga/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangareader_net(self):
    #     urls = {
    #         'success': [
    #             'http://www.mangareader.net/red-storm'
    #         ],
    #         'error': [
    #             'http://www.mangareader.net/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangarussia_com(self):
    #     urls = {
    #         'success': [
    #             'http://www.mangarussia.com/manga/Оставаясь+собой.html'
    #         ],
    #         'error': [
    #             'http://www.mangarussia.com/manga/False-name-manga.html'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangasaurus_com(self):
    #     urls = {
    #         'success': [
    #             'http://mangasaurus.com/manga/3747/upotte'
    #         ],
    #         'error': [
    #             'http://mangasaurus.com/manga/0/upotte'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangasupa_com(self):
    #     urls = {
    #         'success': [
    #             'http://mangasupa.com/manga/rurouni_kenshin_hokkaido_arc'
    #         ],
    #         'error': [
    #             'http://mangasupa.com/manga/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangashin_com(self):
    #     urls = {
    #         'success': [
    #             'http://mangashin.com/lovely_again_today'
    #         ],
    #         'error': [
    #             'http://mangashin.com/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mangatown_com(self):
    #     urls = {
    #         'success': [
    #             'http://www.mangatown.com/manga/trinity_seven/'
    #         ],
    #         'error': [
    #             'http://www.mangatown.com/manga/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_manhuagui_com(self):
    #     urls = {
    #         'success': [
    #             'http://www.manhuagui.com/comic/20568/',
    #             'http://www.manhuagui.com/comic/11730/'  # crypt protect
    #         ],
    #         'error': [
    #             'http://www.manhuagui.com/comic/0/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_mintmanga_com(self):
    #     urls = {
    #         'success': [
    #             'http://mintmanga.com/death_field/'
    #         ],
    #         'error': [
    #             'http://mintmanga.com/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_myreadingmanga_info(self):
    #     urls = {
    #         'success': [
    #             'https://myreadingmanga.info/yamamoto-ataru-lovely-play-kr/'
    #         ],
    #         'error': [
    #             'https://myreadingmanga.info/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_ninemanga_com(self):
    #     urls = {
    #         'success': [
    #             'http://www.ninemanga.com/manga/RESCUE+ME%21.html'
    #         ],
    #         'error': [
    #             'http://www.ninemanga.com/manga/False-name-manga.html'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_read_yagami_me(self):
    #     urls = {
    #         'success': [
    #             'http://read.yagami.me/series/gozen_3ji_no_muhouchitai/'
    #         ],
    #         'error': [
    #             'http://read.yagami.me/series/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_readmanga_me(self):
    #     urls = {
    #         'success': [
    #             'http://readmanga.me/nine_lives/'
    #         ],
    #         'error': [
    #             'http://readmanga.me/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_selfmanga_ru(self):
    #     urls = {
    #         'success': [
    #             'http://selfmanga.ru/my_life'
    #         ],
    #         'error': [
    #             'http://selfmanga.ru/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_shakai_ru(self):
    #     urls = {
    #         'success': [
    #             'http://shakai.ru/manga/2796/'
    #         ],
    #         'error': [
    #             'http://shakai.ru/manga/0/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_somanga_net(self):
    #     urls = {
    #         'success': [
    #             'http://somanga.net/manga/otouto-no-otto'
    #         ],
    #         'error': [
    #             'http://somanga.net/manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_tenmanga_com(self):
    #     urls = {
    #         'success': [
    #             'http://www.tenmanga.com/book/TO+LOVE-RU+DARKNESS.html'
    #         ],
    #         'error': [
    #             'http://www.tenmanga.com/book/False-name-manga.html'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_unixmanga_nl(self):
    #     urls = {
    #         'success': [
    #             'http://unixmanga.nl/onlinereading/Origin.html'
    #         ],
    #         'error': [
    #             'http://unixmanga.nl/onlinereading/False-name-manga.html'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_wmanga_ru(self):
    #     urls = {
    #         'success': [
    #             'http://wmanga.ru/starter/manga_byid/07ghost'
    #         ],
    #         'error': [
    #             'http://wmanga.ru/starter/manga_byid/False-name-manga'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_yaoichan_me(self):
    #     urls = {
    #         'success': [
    #             'http://yaoichan.me/manga/5768--20c-of-love.html'
    #         ],
    #         'error': [
    #             'http://yaoichan.me/manga/1-False-name-manga.html'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_zingbox_me(self):
    #     urls = {
    #         'success': [
    #             'http://www.zingbox.me/manga/6286/Girl+the+Wild\'s'
    #         ],
    #         'error': [
    #             'http://www.zingbox.me/manga/0/Girl+the+Wild\'s'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])
    # 
    # def test_zip_read_com(self):
    #     urls = {
    #         'success': [
    #             'http://zip-read.com/よしまさこ-うてなの結婚/'
    #         ],
    #         'error': [
    #             'http://zip-read.com/False-name-manga/'
    #         ]
    #     }
    #     self._urls_true(urls['success'])
    #     self._urls_false(urls['error'])


if __name__ == '__main__':
    unittest.main()