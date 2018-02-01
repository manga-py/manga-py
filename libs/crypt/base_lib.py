
import base64
import codecs
import gzip
import zlib
from hashlib import md5
from struct import pack, unpack

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from execjs import compile as js_compile


class BaseLib:

    @staticmethod
    def decode_escape(data):

        if isinstance(data, str):
            data = data.encode()
        try:
            data = codecs.escape_decode(data)
            return data[0]
        except Exception:
            return ''

    @staticmethod
    def encode_hex(data):
        return codecs.decode(data, 'hex')

    @staticmethod
    def to_sha_256(data):
        if isinstance(data, str):
            data = data.encode()
        sha = SHA256.new()
        sha.update(data)
        return sha.digest()

    @staticmethod
    def decrypt_aes(iv, key, data):
        aes = AES.new(key, AES.MODE_CBC, iv)
        return aes.decrypt(data)

    @staticmethod
    def base64decode(data, altchars=None, validate=False):
        return base64.b64decode(data, altchars, validate)

    @staticmethod
    def base64encode(data, altchars=None):
        return base64.b64encode(data, altchars)

    @staticmethod
    def exec_js(source, js):
        return js_compile(source).eval(js)

    @staticmethod
    def gunzip(data):
        return gzip.decompress(data)

    @staticmethod
    def gzip(data, lvl: int = 9):
        return gzip.compress(data, lvl)

    @staticmethod
    def zlib_d(data, **kwargs):
        return zlib.decompress(data, **kwargs)

    @staticmethod
    def zlib_c(data, **kwargs):
        return zlib.compress(data, **kwargs)

    @staticmethod
    def md5():
        return md5

    @staticmethod
    def pack(fmt, *args):
        return pack(fmt, *args)

    @staticmethod
    def unpack(fmt, string):
        return unpack(fmt, string)
