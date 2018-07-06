import unittest
from manga_py.provider import Provider
from manga_py.crypt.ac_qq_com import AcQqComCrypt
from manga_py.crypt.kissmanga_com import KissMangaComCrypt


class Crypt(unittest.TestCase):
    _ac_qq_data = "8eyJjb21pYyI6eyJpZCI6NTM2NDM1LCJ0aXRsZSI6Ilx1NTczMFx1ODVjZlx1OWY1MFx1NTkyOSIsImNvbGxlY3QiOiIxNDg3OTU1IiwiaXNKYXBhbkNvbWljIjpmYWxzZSwiaXNMaWdodE5vdmVsIjpmYWxzZSwiaXNMaWdodENvbWljIjpmYWxzZSwiaXNGaW5pc2giOmZhbHNlLCJpc1JvYXN0YWJsZSI6dHJ1ZSwiZUlkIjoiS2xCUFMwTlBYVlZhQWdZZkFRWUFBd3NNSEVKWVhTZz0ifSwiY2hhcHRlciI6eyJjaWQiOjI3NCwiY1RpdGxlIjoiMTI1XHVmZjFhXHU3OGE3XHU5MWNlXHUwMGI3XHU4NTg3XHU1YzlhIFx1NGUwYSIsImNTZXEiOiIyNTUiLCJ2aXBTdGF0dXMiOjIsInByZXZDaWQiOjI3MywibmV4dENpZCI6Mjc1LCJibGFua0ZpcnN0IjoxLCJjYW5SZWFkIjpmYWxzZX0sInBpY3R1cmUiOlt7InBpZCI6IjI4MDM3Iiwid2lkdGgiOjkwMCwiaGVpZ2h0IjoxMjczLCJ1cmwiOiJodHRwczpcL1wvbWFuaHVhLnFwaWMuY25cL21hbmh1YV9kZXRhaWxcLzBcLzI1XzE2XzI0X2U5NTNiZjhhMTBjODA1MWQxNTQyYzA0OWQ0OTdlOTJhXzI4MDM3LmpwZ1wvMCJ9XSwiYWRzIjp7InRvcCI6IiIsImxlZnQiOltdLCJib3R0b20iOnsidGl0bGUiOiJcdTRlMDdcdTRlOGJcdTRlMDdcdTcwNzUiLCJwaWMiOiJodHRwczpcL1wvbWFuaHVhLnFwaWMuY25cL29wZXJhdGlvblwvMFwvMDVfMTFfNDRfYzlhZGZlZGQxMjExNjczNTAyMWEyMmJjYTY2YWVkNDFfMTUzMDc2MjI2NjYxNy5qcGdcLzAiLCJ1cmwiOiJodHRwOlwvXC9hYy5xcS5jb21cL0NvbWljXC9jb21pY0luZm9cL2lkXC82MzEzOTkiLCJ3aWR0aCI6IjY1MCIsImhlaWdodCI6IjExMCJ9fSwiYXJ0aXN0Ijp7ImF2YXRhciI6Imh0dHA6XC9cL3RoaXJkcXEucWxvZ28uY25cL2c/Yj1zZGsmaz03dmg2WVBhSUQzNWRaQzZXMkppYlBFZyZzPTY0MCZ0PTE1MTczNzA2MjkiLCJuaWNrIjoiXHVmZjA4XHU1MTZiXHU1ZWE2XHVmZjA5XHU0ZTAwXHU0ZThjXHU1ZGU1XHU0ZjVjXHU1YmE0IiwidWluQ3J5cHQiOiJkMnRQZG5WV05GZE9XVms5In19"
    _kissmanga_data = "hkJ+EJR/9dCEuATq4edqK2Y2yYuk7oHv6DtMcKdZDztGw8Bdrm3Uh9Z6aZnJeq51IeU04EwWn8DUZ3wEfdvMnYtQh7GSoWdOkdJa7Dbyfs7AspTURTDMhBqYsoZzduP7kyxQ/ftwtbQ733ShihZvNUg4pcR36H4YAKEAcwhZNA0="

    @property
    def _provider(self):
        provider = Provider()
        provider._params['url'] = 'http://example.org'
        return provider

    def test_ac_qq_com(self):
        lib = AcQqComCrypt(self._provider)
        'data from ac.qq.com/ComicView/index/id/536435/cid/274'
        self.assertIsNotNone(lib.decode(self._ac_qq_data).get('comic', None))

    def test_ac_qq_com_none(self):
        lib = AcQqComCrypt(self._provider)
        self.assertIsNone(lib.decode(self._ac_qq_data[5:]).get('comic', None))

    def test_kissmanga(self):
        lib = KissMangaComCrypt()
        'view-source:kissmanga.com/Manga/Kou-1-Desu-ga-Isekai-de-Joushu-Hajimemashita/Chapter-019?id=401994'
        key = b'72nnasdasd9asdn123'
        iv = b'a5e8e2e9c2721be0a84ad660c472c1f3'
        print(lib.decrypt(iv, key, self._kissmanga_data).decode('utf-8').replace('\x10', '').replace('\x0f', ''))
