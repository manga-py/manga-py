#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
import codecs
import re
from hashlib import md5
from os import path
from struct import pack, unpack

import execjs
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


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
    try:
        return execjs.compile(get_manhuagui_com_js()).eval(js)
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
    def unpack(string) -> list:
        """
        :param string: str
        :return: tuple
        """
        if isinstance(string, str):
            string = string.encode()
        return [i for i in string]

    def decrypt_license(self, bid, u1, license_b64) -> bytes:
        """
        :param bid: browser id
        :param u1: got from cookie
        :param license_b64: Base64-encoded license object
        :return: bytes
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
        """
        :param key:
        :param data:
        :return:
        """
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

    @staticmethod
    def gen_rc4_table(key) -> list:
        s = [i for i in range(0, 256)]
        j = 0
        for i in range(0, 256):
            j = (j + s[i] + key[i % len(key)]) & 0xff
            s[i], s[j] = s[j], s[i]
        return s


def get_manhuagui_com_js():  # pragma: no cover
    return """
    var LZString = (function () {
    var f = String.fromCharCode;
    var keyStrBase64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var baseReverseDic = {};

    function getBaseValue(alphabet, character) {
        if (!baseReverseDic[alphabet]) {
            baseReverseDic[alphabet] = {};
            for (var i = 0; i < alphabet.length; i++) {
                baseReverseDic[alphabet][alphabet.charAt(i)] = i
            }
        }
        return baseReverseDic[alphabet][character]
    }

    var LZString = {
        decompressFromBase64: function (input) {
            if (input == null) return "";
            if (input == "") return null;
            return LZString._0(input.length, 32, function (index) {
                return getBaseValue(keyStrBase64, input.charAt(index))
            })
        }, _0: function (length, resetValue, getNextValue) {
            var dictionary = [], next, enlargeIn = 4, dictSize = 4, numBits = 3, entry = "", result = [], i, w, bits,
                resb, maxpower, power, c, data = {val: getNextValue(0), position: resetValue, index: 1};
            for (i = 0; i < 3; i += 1) {
                dictionary[i] = i
            }
            bits = 0;
            maxpower = Math.pow(2, 2);
            power = 1;
            while (power != maxpower) {
                resb = data.val & data.position;
                data.position >>= 1;
                if (data.position == 0) {
                    data.position = resetValue;
                    data.val = getNextValue(data.index++)
                }
                bits |= (resb > 0 ? 1 : 0) * power;
                power <<= 1
            }
            switch (next = bits) {
                case 0:
                    bits = 0;
                    maxpower = Math.pow(2, 8);
                    power = 1;
                    while (power != maxpower) {
                        resb = data.val & data.position;
                        data.position >>= 1;
                        if (data.position == 0) {
                            data.position = resetValue;
                            data.val = getNextValue(data.index++)
                        }
                        bits |= (resb > 0 ? 1 : 0) * power;
                        power <<= 1
                    }
                    c = f(bits);
                    break;
                case 1:
                    bits = 0;
                    maxpower = Math.pow(2, 16);
                    power = 1;
                    while (power != maxpower) {
                        resb = data.val & data.position;
                        data.position >>= 1;
                        if (data.position == 0) {
                            data.position = resetValue;
                            data.val = getNextValue(data.index++)
                        }
                        bits |= (resb > 0 ? 1 : 0) * power;
                        power <<= 1
                    }
                    c = f(bits);
                    break;
                case 2:
                    return ""
            }
            dictionary[3] = c;
            w = c;
            result.push(c);
            while (true) {
                if (data.index > length) {
                    return ""
                }
                bits = 0;
                maxpower = Math.pow(2, numBits);
                power = 1;
                while (power != maxpower) {
                    resb = data.val & data.position;
                    data.position >>= 1;
                    if (data.position == 0) {
                        data.position = resetValue;
                        data.val = getNextValue(data.index++)
                    }
                    bits |= (resb > 0 ? 1 : 0) * power;
                    power <<= 1
                }
                switch (c = bits) {
                    case 0:
                        bits = 0;
                        maxpower = Math.pow(2, 8);
                        power = 1;
                        while (power != maxpower) {
                            resb = data.val & data.position;
                            data.position >>= 1;
                            if (data.position == 0) {
                                data.position = resetValue;
                                data.val = getNextValue(data.index++)
                            }
                            bits |= (resb > 0 ? 1 : 0) * power;
                            power <<= 1
                        }
                        dictionary[dictSize++] = f(bits);
                        c = dictSize - 1;
                        enlargeIn--;
                        break;
                    case 1:
                        bits = 0;
                        maxpower = Math.pow(2, 16);
                        power = 1;
                        while (power != maxpower) {
                            resb = data.val & data.position;
                            data.position >>= 1;
                            if (data.position == 0) {
                                data.position = resetValue;
                                data.val = getNextValue(data.index++)
                            }
                            bits |= (resb > 0 ? 1 : 0) * power;
                            power <<= 1
                        }
                        dictionary[dictSize++] = f(bits);
                        c = dictSize - 1;
                        enlargeIn--;
                        break;
                    case 2:
                        return result.join('')
                }
                if (enlargeIn == 0) {
                    enlargeIn = Math.pow(2, numBits);
                    numBits++
                }
                if (dictionary[c]) {
                    entry = dictionary[c]
                } else {
                    if (c === dictSize) {
                        entry = w + w.charAt(0)
                    } else {
                        return null
                    }
                }
                result.push(entry);
                dictionary[dictSize++] = w + entry.charAt(0);
                enlargeIn--;
                w = entry;
                if (enlargeIn == 0) {
                    enlargeIn = Math.pow(2, numBits);
                    numBits++
                }
            }
        }
    };
    return LZString
})();
String.prototype.splic = function (f) {
    return LZString.decompressFromBase64(this).split(f)
};
    """