from .base_lib import BaseLib
import re
from numpy import isnan


class HoduComicsCom(BaseLib):
    """
    var Base = {
        _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
        encode: function(r) {
            var t, e, o, a, h, n, c, d = "",
                C = 0;
            for (r = Base._utf8_encode(r); C < r.length;) a = (t = r.charCodeAt(C++)) >> 2, h = (3 & t) << 4 | (e = r.charCodeAt(C++)) >> 4, n = (15 & e) << 2 | (o = r.charCodeAt(C++)) >> 6, c = 63 & o, isNaN(e) ? n = c = 64 : isNaN(o) && (c = 64), d = d + this._keyStr.charAt(a) + this._keyStr.charAt(h) + this._keyStr.charAt(n) + this._keyStr.charAt(c);
            return d
        },
        decode: function(r) {
            var t, e, o, a, h, n, c = "",
                d = 0;
            for (r = r.replace(/[^A-Za-z0-9\+\/\=]/g, ""); d < r.length;) t = this._keyStr.indexOf(r.charAt(d++)) << 2 | (a = this._keyStr.indexOf(r.charAt(d++))) >> 4, e = (15 & a) << 4 | (h = this._keyStr.indexOf(r.charAt(d++))) >> 2, o = (3 & h) << 6 | (n = this._keyStr.indexOf(r.charAt(d++))), c += String.fromCharCode(t), 64 != h && (c += String.fromCharCode(e)), 64 != n && (c += String.fromCharCode(o));
            return c = Base._utf8_decode(c)
        },
        _utf8_encode: function(r) {
            r = r.replace(/\r\n/g, "\n");
            for (var t = "", e = 0; e < r.length; e++) {
                var o = r.charCodeAt(e);
                o < 128 ? t += String.fromCharCode(o) : o > 127 && o < 2048 ? (t += String.fromCharCode(o >> 6 | 192), t += String.fromCharCode(63 & o | 128)) : (t += String.fromCharCode(o >> 12 | 224), t += String.fromCharCode(o >> 6 & 63 | 128), t += String.fromCharCode(63 & o | 128))
            }
            return t
        },
        _utf8_decode: function(r) {
            for (var t = "", e = 0, o = c1 = c2 = 0; e < r.length;)(o = r.charCodeAt(e)) < 128 ? (t += String.fromCharCode(o), e++) : o > 191 && o < 224 ? (c2 = r.charCodeAt(e + 1), t += String.fromCharCode((31 & o) << 6 | 63 & c2), e += 2) : (c2 = r.charCodeAt(e + 1), c3 = r.charCodeAt(e + 2), t += String.fromCharCode((15 & o) << 12 | (63 & c2) << 6 | 63 & c3), e += 3);
            return t
        }
    };
    """

    _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    def _utf8_encode(self, r):
        r = re.sub('\r\n', '\n', r)
        t = ''
        for c in r:
            o = ord(c)
            if o < 128:
                t += c
            elif 2048 > o > 127:
                t += chr(o >> 6 | 192)
                t += chr(6 & o | 128)
            else:
                t += chr(o >> 12 | 224)
                t += chr(o >> 6 & 63 | 128)
                t += chr(63 & o | 128)
        return t

    def _utf8_decode(self, r):
        t = ''
        e = 0
        for c in r:
            o = ord(c)
            if o < 128:
                t += c
                e += 1
            elif 224 > o > 191:
                c2 = ord(r[e + 1])
                t += chr((31 & o) << 6 | 63 & c2)
                e += 2
            else:
                c2 = ord(r[e + 1])
                c3 = ord(r[e + 2])
                t += chr((15 & o) << 12 | (63 & c2) << 6 | 63 & c3)
                e += 3
            return t

    def encode(self, r):
        d = ''
        C = 0
        r = self._utf8_encode(r)
        while C < len(r):
            t = ord(r[C])
            C += 1

            a = t >> 2

            e = ord(r[C])
            C += 1

            h = (3 & t) << 4 | e >> 4

            o = ord(r[C])
            C += 1

            n = (15 & e) << 2 | o >> 6

            c = 63 & o

            if isnan(e):
                n = c = 64
            elif isnan(o):
                c = 64

            d += self._keyStr[a] + self._keyStr[h] + self._keyStr[n] + self._keyStr[c]
        return d

    def decrypt(self, r):
        c = ''
        d = 0
        r = re.sub(r'[^A-Za-z0-9+/=]', '', r)
        while d < len(r):
            _t = self._keyStr.find(r[d]) << 2
            d += 1
            a = self._keyStr.find(r[d])
            d += 1
            t = _t | a >> 4

            h = self._keyStr.find(r[d])
            d += 1
            e = (15 & a) << 4 | h >> 2

            n = self._keyStr.find(r[d])
            d += 1
            o = (3 & h) << 6 | n

            c += chr(t)

            if 64 != h:
                c += chr(e)

            if 64 != n:
                c += chr(o)

        return self._utf8_decode(c)
