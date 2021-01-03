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
            self.provider.manga_name,
            '{:0>3}-{}.{}'.format(
                idx, self.provider.get_archive_name(),
                self.provider._archive_type()
            )
        )

    def __download(self, idx, name, url):
        _min, _max = self.provider._min_max_calculate()
        self.provider._info.add_volume(
            self.provider.chapter,
            '%s.%s' % self.provider.get_archive_path()
        )

        self.provider.progress(self.chapters_count, idx)

        if idx < _min or (idx >= _max > 0) or self.is_file(name):
            return False

        if not self.provider._simulate:
            try:
                self.provider.http().download_file(url, name, idx)
            except Exception as e:
                self.provider._info.set_last_volume_error(e)

    def download_archives(self):
        for idx, chap_inf in enumerate(self.provider.chapters):
            try:
                url = chap_inf['download_link']
            except TypeError:
                url = chap_inf

            self.provider.before_download_chapter()
            self.provider.chapter_id = idx
            name = self._get_name(idx)
            idx, url, name = self.before_download(idx, url, name)
            self.__download(idx, name, url)
            self.after_download(idx, name)

    def before_download(self, idx, url, _path):
        return idx, url, _path

    def after_download(self, idx, _path):
        pass
