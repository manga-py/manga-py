import json
import re
from abc import ABC
from sys import stderr
from logging import info, warning, error
from typing import Tuple

from .base_classes import (
    Abstract,
    Archive,
    Base,
    Callbacks,
    cf_scrape,
    Static,
    ArchiveName,
)
from .fs import (
    get_temp_path,
    is_file,
    basename,
    remove_file_query_params,
    path_join,
    file_size,
)
from .http import MultiThreads
from .info import Info
from .meta import repo_url
from .meta import version


class Provider(Base, Abstract, Static, Callbacks, ArchiveName, ABC):
    _volumes_count = 0
    _archive = None
    _zero_fill = False
    _with_manga_name = False
    _info = None
    _simulate = False
    _volume = None
    _show_chapter_info = False
    _debug = False
    _override_name = ''

    def __init__(self, info: Info = None):
        super().__init__()
        self.re = re
        self.json = json
        self._params['temp_directory'] = get_temp_path()
        self._info = info

    def _params_parser(self, params):
        # image params
        self._set_if_not_none(self._image_params, 'crop_blank', params.get('crop_blank', False))
        self._set_if_not_none(
            self._image_params, 'crop',
            (params.get('xt', 0),
             params.get('xr', 0),
             params.get('xb', 0),
             params.get('xl', 0)),
        )
        self._image_params['no_webp'] = params.get('no_webp', False)
        # downloading params
        self._set_if_not_none(self._params, 'destination', params.get('destination', None))
        self._zero_fill = params.get('zero_fill')
        self._with_manga_name = params.get('with_manga_name')
        self._simulate = params.get('simulate')
        self._show_chapter_info = params.get('show_current_chapter_info', False)
        self._debug = params.get('debug', False)
        self._override_name = self._params.get('override_archive_name')
        if self._with_manga_name and self._override_name:
            raise RuntimeError('Conflict of parameters. Please use only --with-manga-name, or --override-archive-name')
        self._fill_arguments(params.get('arguments') or [])

    def process(self, url, params=None):  # Main method
        self._params['url'] = url
        params = params if isinstance(params, dict) else {}
        self._params_parser(params)
        for i in params:
            self._params.setdefault(i, params[i])

        proxy = params.get('proxy', None)
        if proxy is not None:
            self._storage['proxies'] = {
                'http': proxy,
                'https': proxy,
            }

        if self.__manual_ua():
            self.update_ua(self._params['user_agent'])

            cookies = (c.split('=', 1) for c in self._params['cookies'])
            self.update_cookies({c[0]: c[1] for c in cookies})

        self.prepare_cookies()

        info('Manga name: %s' % self.manga_name)
        info('Content length %d' % len(self.content))
        self.chapters = self._prepare_chapters(self.get_chapters())
        info('Chapters received (%d)' % len(self.chapters))

        if not self._params.get('reverse_downloading', False):
            self.chapters = self._storage['chapters'][::-1]

        self._storage['init_cookies'] = self._storage['cookies']

        __ua = self.http().user_agent

        self._info.set_ua(__ua)

        info('User-agent: "%s"' % __ua)

        self.loop_chapters()

    def _check_archive(self):
        # check
        _path = '%s.%s' % self.get_archive_path()
        not_allow_archive = not self._params.get('rewrite_exists_archives', False)

        return not_allow_archive and is_file(_path)

    def _download_chapter(self):
        if not self._simulate:
            try:
                self.before_download_chapter()
                self._storage['files'] = self.get_files()
                self.loop_files()
            except Exception as e:
                # Main debug here
                if self._debug:
                    raise e
                self.log([e], file=stderr)
                self._info.set_last_volume_error(e)

    def loop_chapters(self):
        _min = self._params.get('skip_volumes', 0)
        _max = self._params.get('max_volumes', 0)
        count = 0  # count downloaded chapters
        for idx, __url in enumerate(self.chapters):
            self.chapter_id = idx
            if idx < _min or (count >= _max > 0) or self._check_archive():
                info('Skip chapter %d / %s' % (idx, __url))
                continue

            info('Processed chapter %d / %s' % (idx, __url))

            count += 1
            self._info.add_volume(self.chapter_for_json(), '%s.%s' % self.get_archive_path())
            self._download_chapter()

        if count == 0 and not self.quiet:
            print('No new chapters found', file=stderr)

    def loop_files(self):
        if isinstance(self._storage['files'], list):
            info('Processing {} files'.format(len(self._storage['files'])))

            if self._show_chapter_info:
                print('\n\nCurrent chapter url: %s\n' % (self.chapter,), file=stderr)

            if len(self._storage['files']) == 0:
                # see Std
                error('Error processing file: %s' % self.get_archive_name())
                return

            self._archive = Archive()
            self._archive.not_change_files_extension = self._params.get('not_change_files_extension', False)
            self._archive.no_webp = self._image_params.get('no_webp', False)
            self._call_files_progress_callback()

            self._multi_thread_save(self._storage['files'])

            self.make_archive()
        else:
            error('Bad files list type')

    def _save_file_params_helper(self, url, idx):
        if url is None:
            _url = self.http().normalize_uri(self.get_current_file())
        else:
            _url = url
        _url = self.before_file_save(_url, idx)
        filename = remove_file_query_params(basename(_url))
        _path = self.remove_not_ascii(self._image_name(idx, filename))
        _path = get_temp_path(_path)
        return _path, idx, _url

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        _path, idx, _url = self._save_file_params_helper(url, idx)

        if not is_file(_path) or file_size(_path) < 32:
            self.http().download_file(_url, _path, idx)
        self.after_file_save(_path, idx)
        self._archive.add_file(_path)

        callable(callback) and callback()

        return _path

    def get_archive_path(self) -> Tuple[str, str]:
        if self._override_name:
            _path = "{}_{}".format(self._override_name, str(self.normal_arc_name(self.get_chapter_index().split('-'))))
        else:
            # see Std
            _path = remove_file_query_params(self.get_archive_name())
        _path = self.remove_not_ascii(_path)

        if not _path:
            _path = str(self.chapter_id)

        name = self.name

        additional_data_name = ''
        if self.http().has_error:
            additional_data_name = '.ERROR'
            self.http().has_error = False
            warning('Error processing chapter.')

        return (
            path_join(
                self._params.get('destination', 'Manga'),
                name,
                '%s%s' % (_path, additional_data_name)
            ).replace('?', '_').replace('"', '_').replace('>', '_').replace('<', '_').replace('|', '_')  # Windows...
            , self._archive_type()
        )

    def make_archive(self):
        _path = self.get_archive_path()

        info = 'Site: {}\nDownloader: {}\nVersion: {}'.format(self.get_url(), repo_url, version)

        # """
        # make book info
        # """
        # if self._params['cbz']:
        #     self._archive.add_book_info(self._arc_meta_info())

        self._archive.add_info(info)

        if self._archive.has_error:
            full_path = '%s.IMAGES_SKIP_ERROR.%s' % _path
        else:
            full_path = '%s.%s' % _path

        try:
            self._archive.make(full_path)
        except OSError as e:
            error(e)
            self._info.set_last_volume_error(str(e))
            raise e

    def html_fromstring(self, url, selector: str = None, idx: int = None):
        params = {}
        if isinstance(url, dict):
            params = url['params']
            url = url['url']
        return self.document_fromstring(self.http_get(url, **params), selector, idx)

    def _multi_thread_callback(self):
        self._call_files_progress_callback()
        self._storage['current_file'] += 1

    def _multi_thread_save(self, files):
        threading = MultiThreads()
        # hack
        self._storage['current_file'] = 0
        if self._params.get('max_threads', None) is not None:
            threading.max_threads = int(self._params.get('max_threads'))
        for idx, url in enumerate(files):
            threading.add(self.save_file, (idx, self._multi_thread_callback, url, None))

        threading.start()

    def cf_scrape(self, url):
        """
        WARNING! Thins function replace cookies!
        :param url: str
        :return:
        """
        try:
            params = cf_scrape(url)
            if len(params):
                self.update_cookies(params[0])
                self.update_ua(params[1])
                self._params['cf-protect'] = True
        except Exception:
            if not self.__manual_ua():
                self.log('Please, use --cookie and --user-agent options')

    def __manual_ua(self) -> bool:
        return self._params['cookies'] and len(self._params['cookies']) and self._params['user_agent'] and len(self._params['user_agent'])

    def update_ua(self, ua):
        self._storage['user_agent'] = ua
        self.http().user_agent = ua
        self._info and self._info.set_ua(ua)

    def update_cookies(self, cookies):
        for k in cookies:
            self._storage['cookies'][k] = cookies[k]
            self.http().cookies[k] = cookies[k]
