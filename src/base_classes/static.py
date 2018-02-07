from lxml.html import document_fromstring


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
    def __test_ascii(i):
        o = ord(i)
        _ = 39 < o < 58
        _ = _ or 63 < o < 94
        _ = _ or 96 < o < 127
        return _

    @staticmethod
    def remove_not_ascii(value):
        return "".join(i for i in value if i == '_' or Static.__test_ascii(i))
