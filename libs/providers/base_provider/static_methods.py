import re

from lxml.html import document_fromstring

from libs.fs import basename


class StaticMethods:

    @staticmethod
    def document_fromstring(body, selector: str = None, idx: int = None):
        result = document_fromstring(body)
        if isinstance(selector, str):
            result = result.cssselect(selector)
        if isinstance(idx, int):
            result = result[abs(idx)]
        return result

    @staticmethod
    def _set_if_not_none(var, key, value):
        if value is not None:
            var[key] = value

    @staticmethod
    def re_match(pattern, string, flags=0):
        return re.match(pattern, string, flags)

    @staticmethod
    def re_search(pattern, string, flags=0):
        return re.search(pattern, string, flags)

    @staticmethod
    def basename(_path) -> str:
        return basename(_path)

    @staticmethod
    def remove_not_ascii(str):
        return "".join(i for i in str if 39 < ord(i) < 60 or 63 < ord(i) < 94 or 96 < ord(i) < 127)
