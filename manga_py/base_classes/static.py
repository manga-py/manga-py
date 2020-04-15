from lxml.html import document_fromstring
# from purifier.purifier import HTMLPurifier


class Static:

    # @staticmethod
    # def _clear_html(body):
    #     purifier = HTMLPurifier({
    #         'div': ['*'], 'span': ['*'],
    #         'img': ['*'], 'a': ['*'],
    #         'h1': ['*'], 'h2': ['*'],
    #         'h3': ['*'], 'h4': ['*'],
    #         'h5': ['*'], 'h6': ['*'],
    #     })
    #     return purifier.feed(body)

    @staticmethod
    def document_fromstring(body, selector: str = None, idx: int = None):  # pragma: no cover
        result = document_fromstring(body)  # todo
        if isinstance(selector, str):
            result = result.cssselect(selector)
        if isinstance(idx, int):
            result = result[idx]
        return result

    @staticmethod
    def _set_if_not_none(var, key, value):  # pragma: no cover
        if value is not None:
            var[key] = value

    @staticmethod
    def __test_ascii(i):
        o = ord(i)
        _ = 39 < o < 127
        _ = _ and o not in [42, 47, 92, 94]
        return _ or o > 161

    @staticmethod
    def remove_not_ascii(value):
        return "".join(i for i in value if i == '_' or Static.__test_ascii(i))
