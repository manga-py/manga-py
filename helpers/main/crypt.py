#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64
import codecs


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
