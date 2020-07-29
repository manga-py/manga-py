import re
from typing import List, Union
import json


__all__ = ['AcQqComCrypt', 'AcQqComCrypt26']


_site_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
RE_EXTRACT = re.compile(r'"url":\s*"([^"]+?\.(?:jpg|jpeg|png|webp)[^"]*?)"')
RE_PARTS = re.compile(r'(\d+[a-zA-Z]+)')
RE_INT = re.compile(r'^(\d+)')


def key(data: str, idx: int):
    try:
        char = data[idx]
    except IndexError:
        return 0

    position = _site_key.find(char)
    return position


def _decode(data) -> List[str]:
    data = re.sub(r'[^A-Za-z0-9+/=\\]', '', data)
    a = []
    e = 0
    while e < len(data):
        b = key(data, e)
        e += 1
        d = key(data, e)
        e += 1
        f = key(data, e)
        e += 1
        g = key(data, e)
        e += 1

        b = b << 2 | d >> 4
        d = (d & 15) << 4 | f >> 2
        h = (f & 3) << 6 | g
        a.append(chr(b))

        if f != 64:
            a.append(chr(d))

        if g != 64:
            a.append(chr(h))

    return a


class AcQqComCrypt:
    __slots__ = []

    def decode(self, data):
        return self._sub_dict(''.join(_decode(data)))

    @staticmethod
    def _sub_dict(data):
        try:
            data = re.search(r'picture.*?(\[{.+}\])', data).group(1)
            return json.loads(data)
        except Exception as e:
            return {}


class AcQqComCrypt26:  # v2.6
    __slots__ = []

    @staticmethod
    def decode(data: str) -> str:
        return ''.join(_decode(data))

    @staticmethod
    def remap_content(nonce: str, content: Union[list, str]) -> str:
        _data = list(content)
        parts = RE_PARTS.findall(nonce)
        parts_len = len(parts)

        _replace = re.compile(r'\d+')

        while parts_len > 0:
            parts_len -= 1

            _locate = int(RE_INT.search(parts[parts_len]).group(1)) & 255
            _str = _replace.sub('', parts[parts_len])

            _data = _data[0:_locate] + _data[_locate + len(_str):]

        return ''.join(_data)

    # @staticmethod
    # def extract_images(content: str):
    #     content = content.replace(r'\"', '"').replace(r'\\', '\\')
    #     images = RE_EXTRACT.findall(content)
    #     return [i.replace(r'\/', '/') for i in images]
