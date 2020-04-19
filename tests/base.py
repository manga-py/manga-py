import json
import unittest
from os import path
from requests.cookies import RequestsCookieJar

from manga_py import fs
from manga_py.base_classes import Base, Static

root_path = fs.dirname(path.realpath(__file__))

files_paths = [
    ['/files/img1.jpg', '/temp/img1.jpg'],
    ['/files/img2.png', '/temp/img2.png'],
    ['/files/img3.jpg', '/temp/img3.jpg'],
    ['/files/img4.jpg', '/temp/img4.jpg'],
    ['/files/img5.png', '/temp/img5.png'],
    ['/files/img6.gif', '/temp/img6.gif'],
    ['/files/img7.webp', '/temp/img7.webp'],
]

_httpbin = None


def httpbin(bp: Base, _path: str):
    global _httpbin
    variants = [
        'https://httpbin-sttv.herokuapp.com',
        'https://httpbin-org.herokuapp.com',
        'https://httpbin.org',
    ]
    if _httpbin is None:
        for url in variants:
            response = bp.http().requests(url=url, method='head')
            if response.ok:
                _httpbin = url
                break
    if _httpbin is None:
        raise AttributeError('503. Service temporary unavailable / Path: %s ' % _path)
    return '{}/{}'.format(_httpbin, _path.lstrip('/'))


class TestBaseClass(unittest.TestCase):

    def test_base0(self):
        bp = Base()
        domain = 'http://example.org'
        bp._params['url'] = domain + '/manga/here.html'
        self.assertEqual(bp._params['url'], bp.get_url())
        self.assertEqual(domain, bp.domain)

    def test_base1(self):
        bp = Base()
        self.assertRaises(KeyError, bp.get_url)

    def test_get(self):
        bp = Base()
        bp._params['url'] = 'http://example.org/manga/here.html'
        url = httpbin(bp, 'get')
        self.assertEqual(url, json.loads(bp.http_get(url))['url'])

    def test_post(self):
        bp = Base()
        bp._params['url'] = 'http://example.org/manga/here.html'
        url = httpbin(bp, 'post')
        self.assertEqual(url, json.loads(bp.http_post(url))['url'])

    def test_redirect0(self):
        from urllib.parse import quote
        bp = Base()
        bp._params['url'] = 'http://example.org/manga/here.html'
        url = httpbin(bp, 'redirect-to?url=' + quote(httpbin(bp, 'get?test=1')))
        test_data = {'test': '1'}
        content = bp.http_get(url)
        # print(content)
        self.assertEqual(test_data, json.loads(content)['args'])

    def test_ascii(self):
        string = u'/\\\0@#$⼢⼣⼤abCde123йцуڪڦ'
        normal_string = '@⼢⼣⼤abCde123йцуڪڦ'
        self.assertEqual(Static.remove_not_ascii(string), normal_string)
