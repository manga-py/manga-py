from manga_py.provider import Provider
from .helpers.std import Std
from ..crypt.hentainexus_com import HentaiNexusComCrypt


class HentaiNexusCom(Provider, Std):
    def _code(self):
        return self.re.search(r'/(?:read|view)/(\d+)', self.get_url()).group(1)

    def get_archive_name(self) -> str:
        return 'archive'

    def get_chapter_index(self) -> str:
        return '0'

    def get_content(self):
        return self.http_get('{}/view/{}'.format(self.domain, self._code()))

    def get_manga_name(self) -> str:
        return self.text_content(self.content, 'h1.title')

    def get_chapters(self):
        return [b'0']

    def get_files(self):
        content = self.http_get('{}/read/{}'.format(self.domain, self._code()))
        code = self.re.search(r"""initReader\(['"](.+?)['"]""", content).group(1)

        json_data = self.json.loads(self.helper.decode(code))

        server = json_data['b']
        server_path = json_data['r']
        server_code = json_data['i']

        return ['{}{}{}/{}/{}'.format(
            server,
            server_path,
            i['h'],
            server_code,
            i['p']
        ) for i in json_data['f']]

    def prepare_cookies(self):
        self.helper = HentaiNexusComCrypt()

    def get_cover(self) -> str:
        return self._cover_from_content('.is-one-quarter-fullhd  figure.image > img')


main = HentaiNexusCom
