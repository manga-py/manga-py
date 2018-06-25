from manga_py.meta import __downloader_uri__
from manga_py.provider import Provider


class TapasIo:
    provider = None

    def __init__(self, provider: Provider):
        self.provider = provider

    def _content(self, content):
        type = content.get('type', None)
        if type == 'DEFAULT':
            return self._type_default(content)

    def _error(self, content):
        self.provider.log('\r\nERROR!\r\nCode: {}\r\nType: {}\r\nPlease, send url to developer ({})'.format(
            content['code'],
            content['type'],
            __downloader_uri__
        ))

    def _type_default(self, content):
        items = self.provider.document_fromstring(content.get('data', {}).get('html', '<html></html>'), '.art-image')
        return [i.get('src') for i in items]

    def chapter_url(self):
        return '{}/episode/view/{}'.format(
            self.provider.domain,
            self.provider.chapter['id']
        )

    def parse_chapter_content(self):
        content = self.provider.json.loads(self.provider.http_get(self.chapter_url()))
        if content['code'] != 200:
            self._error(content)
            return []
        _content = self._content(content)
        if _content is None:
            self._error(content)
        return _content
