from re import compile
from requests import get
from requests.exceptions import HTTPError


def check_alternative_server(images: list, other_cdn: str):
    if len(images):
        try:
            with get(images[0], stream=True) as image:
                image.raise_for_status()
        except HTTPError:
            re = compile('^.*//[^/](/.+)$')
            return ['%s%s' % (other_cdn, re.search(i).group(1)) for i in images]
    return images
