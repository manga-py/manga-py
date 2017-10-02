#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from struct import pack, unpack
from hashlib import md5
import re
import base64
import codecs
import execjs
from os import path


def decode_escape(data):
    if isinstance(data, str):
        data = data.encode()
    try:
        data = codecs.escape_decode(data)
        return data[0]
    except Exception:
        return False


def encode_hex(data):
    return codecs.decode(data, 'hex')


def _toSha256(data):
    if isinstance(data, str):
        data = data.encode()
    sha = SHA256.new()
    sha.update(data)
    return sha.digest()


def _decryptAES(iv, key, data):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(data)


def kissmanga(iv, key, data):
    iv = encode_hex(iv)
    key = _toSha256(key)
    data = base64.b64decode(data)

    try:
        return _decryptAES(iv, key, data).decode('utf-8').strip()
    except Exception:
        return False


def manhuagui(js, default=''):
    script = path.join(path.dirname(path.realpath(__file__)), 'manhuagui_com.js')
    try:
        with open(script, 'r') as LZjs:
            return execjs.compile(LZjs.read()).eval(js)
    except execjs._exceptions.RuntimeUnavailableError:
        print('Could not find an available JavaScript runtime. Need install Node.js')
        return default
    except Exception:
        return default


class ComicWalker:
    """
    @see https://github.com/eagletmt/comic_walker/blob/master/lib/comic_walker/cipher.rb
    """
    BASE_KEY = None

    def __init__(self):
        key = [173, 43, 117, 127, 230, 58, 73, 84, 154, 177, 47, 81, 108, 200, 101, 65]
        self.BASE_KEY = self.pack(key)

    @staticmethod
    def pack(int_list) -> bytes:
        """
        :param int_list: list
        :return: str
        """
        base_frm = '{}B'.format(len(int_list))
        return pack(base_frm, *int_list)

    @staticmethod
    def unpack(string) -> tuple:
        """
        :param string: str
        :return: tuple
        """
        return unpack('B', string.encode())

    def decrypt_license(self, bid, u1, license_b64) -> bytes:
        """
        :param bid: browser id
        :param u1: got from cookie
        :param license_b64: Base64-encoded license object
        :return: str
        """
        h = [ord(i) for i in bid]
        if u1:
            h += [ord(i) for i in u1]
        return self.decrypt_b64(self.pack(h) + self.BASE_KEY, license_b64.encode())

    def decrypt_b64(self, key, b64data) -> bytes:
        """
        :param key: key
        :param b64data: Encrypted Base64-encoded data
        :return: Decrypted data
        """
        data = base64.b64decode(b64data)
        md5sum = md5()
        md5sum.update(key + data[8:8])
        md5sum = md5sum.hexdigest()
        lt = re.findall('(..)', md5sum)
        lt = [int(i, 16) for i in lt]
        rc4 = self.decrypt_rc4(lt, self.unpack(data[-16:]))
        return self.pack(rc4)

    def decrypt_rc4(self, key, data) -> list:
        s = self.gen_rc4_table(key)
        i = 0
        j = 0
        result = []
        for x in data:
            i = (i + 1) & 0xff
            j = (j + s[i]) & 0xff
            s[i], s[j] = s[j], s[i]
            k = s[(s[i] + s[j]) & 0xff]
            result.append(x ^ k)
        return result

    def gen_rc4_table(self, key) -> list:
        pass

    def comicwalker(self):
        pass
