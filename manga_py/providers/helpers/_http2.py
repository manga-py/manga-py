
class Http2:
    provider = None
    path_join = None
    is_file = None

    def __init__(self, provider):
        from manga_py.fs import path_join, is_file
        self.provider = provider
        self.path_join = path_join
        self.is_file = is_file

    def _get_name(self, url):
        archive = self.provider._params.get('name', '')
        if not len(archive):
            archive = self.provider._storage['manga_name']
        return self.path_join(
            self.provider._params.get('destination', 'Manga'),
            archive,
            url[0]
        )

    def download_archives(self):
        volumes = self.provider._storage['chapters']
        _min = self.provider._params.get('skip_volumes', 0)
        _max = _min + self.provider._params.get('max_volumes', 0)
        for idx, url in enumerate(volumes):
            self.provider._storage['current_chapter'] = idx
            name = self._get_name(url)
            if idx < _min or (idx > _max > 0) or self.is_file(name):
                continue
            self.provider.http().download_file(url[1], name)
