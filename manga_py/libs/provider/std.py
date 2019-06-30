from typing import Union, List, Optional

from lxml.html import HtmlElement, document_fromstring


class Std:
    @staticmethod
    def elements(content: HtmlElement, selector: str, idx: int = None) -> Union[List[HtmlElement], HtmlElement]:
        elements = content.cssselect(selector)  # type: List[HtmlElement]
        if idx is not None:
            return elements[idx]
        return elements

    @staticmethod
    def element_arg(
            content: List[HtmlElement], attr: str, idx: int = None, default: str = None
    ) -> Optional[List[str]]:
        if idx is not None:
            try:
                element = content[idx]
            except IndexError:
                raise IndexError('Index %d not exists' % idx)
            return [element.get(attr, default)]
        return [i.get(attr, default) for i in content]

    @staticmethod
    def document_fromstring(content: str, selector: str = None,
                            idx: int = None) -> Union[HtmlElement, List[HtmlElement]]:
        result = document_fromstring(content)  # type: HtmlElement
        if selector is not None:
            result = result.cssselect(selector)
        if idx is not None:
            result = result[idx]
        return result

    @staticmethod
    def remove_non_printing_characters(value):
        def test(i: str):
            o = ord(i)
            _ = (39 < o < 127) or o > 161
            return _ and o not in [42, 47, 92, 94]
        return "".join(i for i in value if i == '_' or test(i))

    @staticmethod
    def images(content: List[HtmlElement], attr: str, alt_attr: str = None) -> List[str]:
        return [i.get(attr, i.get(alt_attr)) for i in content]

    @staticmethod
    def first_select_options(content: HtmlElement, selector: str, skip_first=True, idx: int = 0) -> List[HtmlElement]:
        options = 'option'
        if skip_first:
            options = 'option + option'
        select = content.cssselect(selector)  # type: List[HtmlElement]
        if len(select) < (idx + 1):
            raise RuntimeError('Select with index %d not found' % idx)
        return select[idx].cssselect(options)

    @staticmethod
    def text_content(element: HtmlElement, strip: bool = True):
        text = element.text_content()
        return text.strip() if strip else text
