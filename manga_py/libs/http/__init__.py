from pathlib import Path

from requests import Response

from manga_py.libs.log import logger
from manga_py.libs.store import Store


class Htpp:
    __slots__ = ()
    __store = Store()

    def __init__(self, args):
        pass

    def download(self, response: Response, destination: Path):
        logger.debug()

        with destination.open('wb') as w:
            if not w.writable():
                raise



