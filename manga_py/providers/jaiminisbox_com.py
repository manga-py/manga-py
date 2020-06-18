from .gomanga_co import GoMangaCo
from re import MULTILINE
from manga_py.crypt.base_lib import BaseLib


class JaiMiniBox(GoMangaCo):

    def get_files(self):
        self._go_chapter_content = self.http_get(self.chapter)

        selector = self.re.search(r'page_width\s=\sparseInt\((\w+)\[', self._go_chapter_content).group(1)
        selector_content = r'^\s*(.+var\s{}\s*=.+)$'.format(selector)

        atob = """
        const btoa = (str) => Buffer.from(str).toString('base64');
        const atob = (b64Encoded) => Buffer.from(b64Encoded, 'base64').toString('utf8');
        """

        content = self.re.search(selector_content, self._go_chapter_content, MULTILINE).group(1)

        items = BaseLib.exec_js('{}{}'.format(atob, content), 'JSON.stringify({})'.format(selector))

        items = self.json.loads(items)

        return [i.get('url') for i in items]


main = JaiMiniBox
