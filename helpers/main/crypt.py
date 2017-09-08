#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Crypto.Cipher as Cipher
import Crypto.Hash as Hash
import base64
import codecs

# a = AES.new(_toSha256, AES.MODE_CBC, codecs.decode('a5e8e2e9c2721be0a84ad660c472c1f3', 'hex'))


def _toSha256(data):
    return Hash.SHA256.new(Hash.SHA256.tobytes('mshsdf832nsdbash20asdm')).digest()


def _toAES(iv, key, data):
    pass


def kissmanga(data):
    d = base64.b64decode(data)
    return _toSha256(d)
