
import base64
import codecs
import re
from hashlib import md5
from os import path
from struct import pack, unpack

import execjs
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


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
