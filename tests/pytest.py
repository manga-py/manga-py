#!/usr/bin/python3
# -*- coding: utf-8 -*-


import unittest


class Test(unittest.TestCase):
    def setUp(self):
        self.current_id = ''
        pass

    def _error_url(self, url):
        pass

    def _next_url_true(self, url):
        pass

    def _next_url_false(self, url):
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
