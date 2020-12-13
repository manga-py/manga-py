from logging import error
from urllib.parse import urlparse


class ProviderParams:
    @property
    def content(self):
        content = self._storage.get('main_content', None)
        if content is None:
            content = self.get_content()
        return content

    @property
    def manga_name(self) -> str:
        name = self._storage.get('manga_name', None)
        if name is None:
            name = self.get_manga_name()
        return name

    @property
    def name(self) -> str:
        name = self._params.get('name', '')
        if not len(name):
            name = self.manga_name
        return name

    @property
    def domain(self) -> str:
        _url = self._params['url']
        try:
            if not self._storage.get('domain_uri', None):
                parsed = urlparse(_url, 'https')
                self._storage['domain_uri'] = '{}://{}'.format(
                    parsed.scheme,
                    parsed.netloc
                )
            return self._storage.get('domain_uri', '')
        except Exception:
            error('url "%s" is broken!' % _url)
            exit()

    @property
    def chapter(self):
        return self.chapters[self.chapter_id]

    @property
    def chapters(self):
        return self._storage['chapters']

    @chapters.setter
    def chapters(self, chapters: list):
        self._storage['chapters'] = chapters
