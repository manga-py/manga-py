from manga_py.provider import Provider
from .helpers.std import Std
from logging import warning, error
import re
import itertools


RE_APP = re.compile(r'App\s?=\s?({.+?})[;<]')


class ReMangaOrg(Provider, Std):
    def get_archive_name(self) -> str:
        return self.normal_arc_name({
            'vol': str(self.chapter['tome']),
            'ch': str(self.chapter['chapter']).split('.'),
        })

    def get_chapter_index(self) -> str:
        return str(self.chapter['index'])

    def get_content(self):
        js_data = RE_APP.search(self._get_content('{}/manga/{}')).group(1)
        return self.json.loads(js_data)

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        with self.http().get(
            self._api_url('/titles/chapters/?branch_id=%d' % self._branch_id)
        ) as resp:
            data = resp.json()

        paid_chapters = len([ch for ch in data['content'] if ch['is_paid']])
        if paid_chapters:
            self.log('Found %d paid chapters. Please, check site on your browser' % paid_chapters)

        return [ch for ch in data['content'] if not ch['is_paid']]

    def _api_url(self, sub_url: str):
        return '{}{}'.format(
            self.content['apiUrl'].rstrip('/'),
            sub_url
        )

    def get_files(self):
        try:
            with self.http().get(
                self._api_url('/titles/chapters/{}'.format(
                    self.chapter['id']
                ))
            ) as resp:
                pages = resp.json().get('content', {}).get('pages', [])
                if len(pages) == 0:
                    warning('Pages list has empty')
                    return []

                if type(pages[0]) == list:
                    images = list(itertools.chain(
                        *pages
                    ))
                else:
                    images = pages

            return [img['link'] for img in images]

        except Exception as e:
            warning(str(e))
            return []

        # content = self._get_content(
        #     '{}/manga/{}/ch%d' % self.chapter['id']
        # )
        #
        # js_data = RE_APP.search(content).group(1)
        # json_data = self.json.loads(js_data)
        #
        # images = self._content_value([
        #     'state',
        #     'chapter',
        #     'content',
        #     'data',
        #     'pages',
        # ], json_data)
        #
        # return [img['link'] for img in sorted(images, key=lambda x: x['page'])]

    @property
    def _branch_id(self):
        branches = self._content_value([
            'state',
            'manga',
            'content',
            'data',
            'branches',
        ])
        if len(branches) == 0:
            error('Branches list has empty')
            return []
        if len(branches) > 1:
            warning('Branches list too long. Please, report this url to')

        return branches[0]['id']

    def _content_value(self, keys: list, content=None):
        data = content or self.content
        for key in keys:
            data = data.get(key, {})
        return data

    def get_cover(self) -> str:
        return self._content_value([
            'state',
            'manga',
            'content',
            'data',
            'img',
            'high',
        ])


main = ReMangaOrg
