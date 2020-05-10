import re
import json

_site_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


def key(char: str):
    position = _site_key.find(char)
    return position


class AcQqComCrypt:
    __slots__ = []

    def decode(self, data):
        data = re.sub(r'[^A-Za-z0-9%+/=\\]', '', data)
        a = []
        e = 0
        while e < len(data) - 3:
            b = key(data[e])
            e += 1
            d = key(data[e])
            e += 1
            f = key(data[e])
            e += 1
            g = key(data[e])
            e += 1

            b = b << 2 | d >> 4
            d = (d & 15) << 4 | f >> 2
            h = (f & 3) << 6 | g
            a.append(chr(b))

            if f != 64:
                a.append(chr(d))

            if g != 64:
                a.append(chr(h))

        return self._sub_dict(''.join(a))

    def _sub_dict(self, data):
        try:
            data = re.search(r'picture.*?(\[{.+}\])', data).group(1)
            return json.loads(data)
        except Exception as e:
            return {}
