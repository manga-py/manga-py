import json
from concurrent.futures import ThreadPoolExecutor
from logging import info, warning, error
from sys import stderr

from PIL import Image

from .base_classes import Archive
from .base_classes.comic_info_builder import Page, ComicInfo
from .fs import (
    is_file,
    file_size,
)
from .meta import repo_url, version


class BaseDownloadMethod(object):
    def __init__(self, provider):
        self.files = []
        self.provider = provider
        self.log = provider.log
        self.http = self.provider.http
        self.chapter_progress = self.provider.chapter_progress
        self.global_progress = self.provider.global_progress
        self.volume = "0"

    def download_chapter(self, url, path):
        pass

    def already_downloaded(self):
        # check
        _path = '%s.%s' % self.provider.get_archive_path()
        not_allow_archive = not self.provider._params.get('rewrite_exists_archives', False)

        return not_allow_archive and is_file(_path)


class OnePerOneDownloader(BaseDownloadMethod):
    chapter_url = None
    path = None
    _archive = None

    def __init__(self, provider):
        super().__init__(provider)
        self.__pages_cache = []

    def download_chapter(self, chapter_url, path):
        self.chapter_url = chapter_url
        self.path = path
        self.__pages_cache = []
        try:
            self.files = self.provider.get_files()
            self._loop_files()
        except Exception as e:
            # Main debug here
            if self.provider._debug:
                raise e
            self.log([e], file=stderr)
            self.provider._info.set_last_volume_error(e)

    def _loop_files(self):
        if isinstance(self.files, list):
            info('Processing {} files'.format(len(self.files)))

            if len(self.files) == 0:
                # see Std
                error('Error processing file: %s' % self.provider.get_archive_name())
                return

            self._archive = Archive()
            self._archive.not_change_files_extension = self.provider._params.get('not_change_files_extension', False)
            self._archive.no_webp = self.provider._image_params.get('no_webp', False)

            if self.provider._save_chapter_info:
                self._archive.write_file('info.json', json.dumps(self.chapter_url))

            chapter_info = self.provider.chapter_details(self.chapter_url)
            if self.provider._save_chapter_info:
                if chapter_info is not None:
                    self._archive.write_file('eduhoribe.json', json.dumps(chapter_info))
                else:
                    warning('No chapter details was found!')
                    warning('Possibly the provider has not yet been implemented to get this information')

            self.chapter_progress(len(self.files), 0, True)

            self._multi_thread_save(self.files)

            self._make_archive()
        else:
            error('Bad files list type')

    def _make_archive(self):
        # """
        # make book info
        # """
        if self.provider._params['cbz']:
            _info = self._book_info_xml()
            self._archive.write_file('ComicInfo.xml', str(_info))

        info = 'Site: {}\nDownloader: {}\nVersion: {}'.format(self.provider.get_url(), repo_url, version)

        self._archive.write_file('info.txt', info)

        if self._archive.has_error:
            full_path = '%s.IMAGES_SKIP_ERROR.%s' % self.path
            self.provider._info.set_last_volume_error(str(self._archive.error_list))
            if self.provider._skip_incomplete_chapters:
                warning("Skipping incomplete chapter: %s.%s" % self.path)
                return
        else:
            full_path = '%s.%s' % self.path

        try:
            self._archive.make(full_path)
        except OSError as e:
            error(e)
            self.provider._info.set_last_volume_error(str(e))
            raise e

    def _multi_thread_save(self, files):
        max_threads = int(self.provider._params.get('max_threads', 0))
        max_threads = min(max(max_threads, 1), 10)

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            m = executor.map(self.save_file, *zip(*enumerate(files)))
            for i, p in enumerate(m, start=1):
                self.chapter_progress(len(self.files), i)

    def save_file(self, idx=None, url=None, callback=None, in_arc_name=None):
        _path, idx, _url = self.provider.before_download_file(idx, url)

        if _path is None:
            return

        if not is_file(_path) or file_size(_path) < 32:
            self.http().download_file(_url, _path, idx)

        _path, _in_arc_name = self.provider.after_file_save(_path, idx)

        if _path is None:
            info('after_file_save is None. Idx: {} / Url: {}'.format(idx, url), file=stderr)
            return None

        self._archive.add_file(_path, in_arc_name=(_in_arc_name or in_arc_name))
        callable(callback) and callback()

        if self.provider._params['cbz']:
            with Image.open(_path) as r:  # type: Image.Image
                w, h = r.size

            self.__pages_cache.append(Page(
                index=idx,
                size=file_size(_path),
                width=w,
                height=h,
            ))

        return _path

    def _book_info_xml(self):
        comic_info = ComicInfo()

        comic_info.number(self.provider.get_chapter_index())
        comic_info.title(self.provider.name)
        comic_info.pages(self.__pages_cache)
        comic_info.page_count(str(len(self.__pages_cache)))

        return comic_info


class WholeArchiveDownloader(BaseDownloadMethod):
    def download_chapter(self, chapter_url, path):
        self.provider.chapter_progress(1, 0, True)
        try:
            self.provider.http().download_file(chapter_url, '%s.%s' % path)
        except Exception as e:
            if self.provider._debug:
                raise e
            self.log([e], file=stderr)
            self.provider._info.set_last_volume_error(e)
        self.provider.chapter_progress(1, 1)

        # if isinstance(self._storage['files'], list):
        #     info('Processing {} files'.format(len(self._storage['files'])))
        #
        # self.__images_cache = []
        #
        # # ///
        #
        # if not is_file(_path) or file_size(_path) < 32:
        #     self.http().download_file(_url, _path, idx)
        #
        # self.after_file_save(_path, idx)
        # self._archive.add_file(_path)
        #
        # with Image.open(_path) as r:  # type: Image.Image
        #     w, h = r.size
        #
        # self.__images_cache.append(Page(
        #     index=idx,
        #     size=file_size(_path),
        #     width=w,
        #     height=h,
        # ))
        #
        # callable(callback) and callback()

    def make_archive(self):
        _path = self.get_archive_path()

        info = 'Site: {}\nDownloader: {}\nVersion: {}'.format(self.get_url(), repo_url, version)

        # """
        # make book info
        # """
        # if self._params['cbz']:
        #     self._archive.add_book_info(self._arc_meta_info())

        self._archive.write_file('info.txt', info)

        if 'cbz' in self._params and self._params['cbz']:
            book_info = ComicInfo()
            book_info.title(self.get_manga_name()) # todo: normal title maybe?
            book_info.pages(self.__images_cache)

            self._archive.write_file('ComicInfo.xml', str(book_info))

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

