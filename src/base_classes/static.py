import re

from lxml.html import document_fromstring

from src.fs import basename


class Static:

    @staticmethod
    def document_fromstring(body, selector: str = None, idx: int = None):  # pragma: no cover
        result = document_fromstring(body)
        if isinstance(selector, str):
            result = result.cssselect(selector)
        if isinstance(idx, int):
            result = result[abs(idx)]
        return result

    @staticmethod
    def _set_if_not_none(var, key, value):  # pragma: no cover
        if value is not None:
            var[key] = value

    @staticmethod
    def remove_not_ascii(value):
        return "".join(i for i in value if 39 < ord(i) < 60 or 63 < ord(i) < 94 or 96 < ord(i) < 127 or i == '_')
