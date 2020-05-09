from re import compile
from requests import get
from requests.exceptions import HTTPError

RE = compile('^https?://[^/]+(/.+)$')


def check_alternative_server(images: list, other_cdn: str, **kwargs):
    if len(images):
        try:
            with get(images[0], stream=True, **kwargs) as image:
                image.raise_for_status()
        except HTTPError:
            return ['%s%s' % (other_cdn, RE.search(i).group(1)) for i in images]
    return images
