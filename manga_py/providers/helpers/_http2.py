
class Http2:
    provider = None
    path_join = None
    is_file = None
    chapters = None
    chapters_count = 0

    def __init__(self, provider):
        from manga_py.fs import path_join, is_file
        self.provider = provider
        self.path_join = path_join
        self.is_file = is_file

    def _get_name(self, idx):
        return self.path_join(
            self.provider._params.get('destination'),
            self.provider._storage['manga_name'],
            '{:0>3}-{}.{}'.format(
                idx, self.provider.get_archive_name(),
                self.provider._archive_type()
            )
        )

    def __download(self, idx, name, url):
        _min, _max = self._min_max_calculate()
        self.provider._info.add_volume(
            self.provider.chapter,
            self.provider.get_archive_path()
        )

        self.provider.progress(self.chapters_count, idx)

        if idx < _min or (idx >= _max > 0) or self.is_file(name):
            return False

        if not self.provider._simulate:
            try:
                self.provider.http().download_file(url, name, idx)
            except Exception as e:
                self.provider._info.set_last_volume_error(e)

    def _min_max_calculate(self):
        _min = self.provider._params.get('skip_volumes', 0)
        _max = self.provider._params.get('max_volumes', 0)
        self.chapters_count = len(self.chapters)
        if _max > 0 or _min > 0:
            if _max < self.chapters_count:
                _max = self.chapters_count - _max
            else:
                _max = 0
            self.chapters_count = self.chapters_count - _min - _max
        if _max > 0 and _min > 0:
            _max += _min - 1
        return _min, _max

    def download_archives(self, chapters=None):
        if chapters is None:
            chapters = self.provider._storage['chapters']
        self.chapters = chapters
        for idx, url in enumerate(chapters):
            self.provider.before_download_chapter()
            self.provider._storage['current_chapter'] = idx
            name = self._get_name(idx)
            idx, url, name = self.before_download(idx, url, name)
            self.__download(idx, name, url)
            self.after_download(idx, name)

    def before_download(self, idx, url, _path):
        return idx, url, _path

    def after_download(self, idx, _path):
        pass
