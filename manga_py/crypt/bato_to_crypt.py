from .base_lib import BaseLib
import re
import pathlib


RE_BATOJS = re.compile(r'\w batojs\s*=\s*(.+);')
RE_SERVER = re.compile(r'\w server\s*=\s*"(.+)";')


class BatoToCrypt(BaseLib):
    @classmethod
    def decrypt_server(cls, page_content: str) -> str:  # pragma: no cover
        batojs = RE_BATOJS.search(page_content).group(1)
        server = RE_SERVER.search(page_content).group(1)

        return cls._server(server, batojs)

    @classmethod
    def _server(cls, server, key):
        with pathlib.Path(__file__).parent.absolute().joinpath('aes.js').open('r') as r:
            script = r.read()
        ev = f"""CryptoJS.AES.decrypt("{server}", ({key}).toString()).toString(CryptoJS.enc.Utf8)"""
        return cls.exec_js(script, ev)
