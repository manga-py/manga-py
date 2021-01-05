import json
from logging import info, warning, error
from sys import stderr

from .base_classes import Archive
from .fs import (
    get_temp_path,
    is_file,
    basename,
    remove_file_query_params,
    path_join,
    file_size,
)
from .http import MultiThreads
from .meta import repo_url, version

class BaseDownloadMethod(object):
    def __init__(self, provider):
        self.provider = provider
        self.http = self.provider.http

    def download_chapter(self, idx, url, path):
        pass

    def before_download(self, idx, url, path):
        return idx, url, path

    def after_download(self, idx, path):
        pass

    def already_downloaded(self, idx):
        # check
        _path = '%s.%s' % self.provider.get_archive_path()
        not_allow_archive = not self.provider._params.get('rewrite_exists_archives', False)

        return not_allow_archive and is_file(_path)

class OnePerOneDownloader(BaseDownloadMethod):
    def __init__(self, provider):
        super().__init__(provider)
        self._call_files_progress_callback = provider._call_files_progress_callback

    def download_chapter(self, idx, url, path):
        try:
            self.provider.before_download_chapter()
            self.files = self.provider.get_files()
            self.provider._storage['files'] = self.files
            self._loop_files()
        except Exception as e:
            # Main debug here
            if self.provider._debug:
                raise e
            self.provider.log([e], file=stderr)
            self.provider._info.set_last_volume_error(e)

    def _loop_files(self):
        self.chapter = self.provider.chapter
        if isinstance(self.files, list):
            info('Processing {} files'.format(len(self.files)))

            if len(self.files) == 0:
                # see Std
                error('Error processing file: %s' % self.get_archive_name())
                return

            self._archive = Archive()
            self._archive.not_change_files_extension = self.provider._params.get('not_change_files_extension', False)
            self._archive.no_webp = self.provider._image_params.get('no_webp', False)

            if self.provider._save_chapter_info:
                self._archive.write_file('info.json', json.dumps(self.chapter))

            chapter_info = self.provider.chapter_details(self.chapter)
            if self.provider._save_chapter_info:
                if chapter_info is not None:
                    self._archive.write_file('eduhoribe.json', json.dumps(chapter_info))
                else:
                    warning('No chapter details was found!')
                    warning('Possibly the provider has not yet been implemented to get this information')

            self._call_files_progress_callback()

            self._multi_thread_save(self.files)

            self._make_archive()
        else:
            error('Bad files list type')

    def _make_archive(self):
        _path = self.provider.get_archive_path()

        info = 'Site: {}\nDownloader: {}\nVersion: {}'.format(self.provider.get_url(), repo_url, version)

        # """
        # make book info
        # """
        # if self._params['cbz']:
        #     self._archive.add_book_info(self._arc_meta_info())

        self._archive.add_info(info)

        if self._archive.has_error:
            full_path = '%s.IMAGES_SKIP_ERROR.%s' % _path
            self._info.set_last_volume_error(str(self._archive.error_list))
            if self._skip_incomplete_chapters:
                warning("Skipping incomplete chapter: %s.%s" % _path)
                return
        else:
            full_path = '%s.%s' % _path

        try:
            self._archive.make(full_path)
        except OSError as e:
            error(e)
            self._info.set_last_volume_error(str(e))
            raise e

    def _multi_thread_callback(self):
        self._call_files_progress_callback()
        self.provider._storage['current_file'] += 1

    def _multi_thread_save(self, files):
        threading = MultiThreads()
        # hack
        self.provider._storage['current_file'] = 0
        if self.provider._params.get('max_threads', None) is not None:
            threading.max_threads = int(self.provider._params.get('max_threads'))
        for idx, url in enumerate(files):
            threading.add(self.save_file, (idx, self._multi_thread_callback, url, None))

        threading.start()

    def _save_file_params_helper(self, url, idx):
        if url is None:
            _url = self.http().normalize_uri(self.get_current_file())
        else:
            _url = url
        _url = self.provider.before_file_save(_url, idx)
        filename = remove_file_query_params(basename(_url))
        _path = self.provider.remove_not_ascii(self.provider._image_name(idx, filename))
        _path = get_temp_path(_path)
        return _path, idx, _url

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        _path, idx, _url = self._save_file_params_helper(url, idx)

        if not is_file(_path) or file_size(_path) < 32:
            self.http().download_file(_url, _path, idx)
        self.provider.after_file_save(_path, idx)
        self._archive.add_file(_path)
        callable(callback) and callback()

        return _path

class WholeArchiveDownloader(BaseDownloadMethod):
    def download_chapter(self, idx, url, path):
        self.provider.chapter_progress(1, 0, True)
        self.provider.before_download_chapter()
        try:
            self.provider.http().download_file(url, path, idx)
        except Exception as e:
            if self.provider._debug:
                raise e
            self.provider.log([e], file=stderr)
            self.provider._info.set_last_volume_error(e)
        self.provider.chapter_progress(1, 1)
