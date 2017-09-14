#!/usr/bin/python3
# -*- coding: utf-8 -*-


import unittest
from os import path, mkdir
import shutil


class Arguments:
    def setArgument(self, name, value):
        setattr(self, name, value)

    def setArguments(self, arguments):
        for name, value in arguments:
            self.setArgument(name, value)


class TestCase(unittest.TestCase):
    def setUp(self):
        import manga
        self.current_id = ''
        self.path = path.join(path.dirname(path.realpath(__file__)), 'temp')
        if not path.isdir(self.path):
            mkdir(self.path)

        self.arguments = Arguments()
        self.arguments.setArguments([  # default arguments
            # ('url', None),
            ('name', 'Manga'),
            ('destination', self.path),
            ('info', False),
            ('progress', False),
            ('skip_volumes', 0),
            ('user_agent', False),
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

    def _error_url(self, url):
        pass

    def _next_url_true(self, url):
        pass

    def _next_url_false(self, url):
        pass

    def _next_test(self, config):
        pass

    def test_balumanga_com(self):
        urls = {
            'success': [  # Site bad! There may be errors
                'http://bulumanga.com/mangaView.html?id=1&cid=34701&page=1&source=mangareader'
                'http://bulumanga.com/introduce.html?id=34701&source=mangareader',
            ],
            'error': [
                'http://bulumanga.com/introduce.html?id=0'
            ],
        }

    def test_com_x_life(self):
        urls = {
            'success': [  # Site bad! There may be errors
                'https://com-x.life/4156-teenage-mutant-ninja-turtles-universe.html'
                'https://com-x.life/3882-grendel.html',
            ],
            'error': [
                'https://com-x.life/0-none.html'
                'https://com-x.life/0-false.html'
            ],
        }

    def test_bato_to(self):
        urls = {
            'success': [  # Site bad! There may be errors
                'https://bato.to/comic/_/comics/karakai-jouzu-no-takagi-san-r13108'
                'https://bato.to/comic/_/comics/mousou-telepathy-r19915',
            ],
            'error': [
                'https://bato.to/comic/omics/mousou-telepathy-r19915'
            ],
        }

if __name__ == '__main__':
    unittest.main()