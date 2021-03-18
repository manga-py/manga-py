import json
import os
import re
from abc import ABC
from logging import info, warning
from os import path
from sys import stderr
from typing import Tuple

from .base_classes import (
    Abstract,
    Base,
    Callbacks,
    cf_scrape,
    Static,
    ArchiveName,
)
from .download_methods import OnePerOneDownloader
from .fs import (
    get_temp_path,
    basename,
    remove_file_query_params,
    path_join,
)
from .info import Info


class Provider(Base, Abstract, Static, Callbacks, ArchiveName, ABC):
    _volumes_count = 0
    _archive = None
    _zero_fill = False
    _with_manga_name = False
    _info = None
    _simulate = False
    _volume = None
    _show_chapter_info = False
    _save_chapter_info = False
    _save_manga_info = False
    _debug = False
    _override_name = ''
    _downloader = OnePerOneDownloader
    global_progress = None

    __images_cache = []

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
        self._show_chapter_info = params.get('show_chapter_info', False)
        self._save_chapter_info = params.get('save_chapter_info', False)
        self._save_manga_info = params.get('save_manga_info', False)
        self._debug = params.get('debug', False)
        self._override_name = self._params.get('override_archive_name')
        if self._with_manga_name and self._override_name:
            raise RuntimeError('Conflict of parameters. Please use only --with-manga-name, or --override-archive-name')
        self._fill_arguments(params.get('arguments') or [])
        self._skip_incomplete_chapters = params.get('skip_incomplete_chapters', False)

    def process(self, url, params=None):  # Main method
        self.prepare_download(url, params)
        self.loop_chapters()

    def prepare_download(self, url, params=None):
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

        if self._save_manga_info:
            details = self.manga_details()
            if details is not None:
                manga_info_path = path.abspath(path.join(self.get_archive_path()[0], os.pardir))
                path.isdir(manga_info_path) or os.makedirs(manga_info_path)

                with open(path.join(manga_info_path, 'info.json'), 'w') as manga_info_file:
                    manga_info_file.write(json.dumps(self.manga_details()))

            else:
                warning('No manga details was found!')
                warning('Possibly the provider has not yet been implemented to get this information')

    def _min_max_calculate(self):
        nb_chapters = len(self.chapters)
        _min = self._params.get('skip_volumes', 0)
        _max = self._params.get('max_volumes', 0)
        # Beware, 0 can also come from command line param
        _max = _max if _max else nb_chapters
        _max = min(nb_chapters, _max + _min)
        self.chapters_count = _max - _min
        return _min, _max

    def loop_chapters(self):
        _min, _max = self._min_max_calculate()
        count = 0  # count downloaded chapters
        for idx, __url in enumerate(self.chapters[:_min], start=1):
            info('Skip chapter %d / %s' % (idx, __url))

        dl = self._downloader(self)

        if callable(self.global_progress):
            self.global_progress(self.chapters_count, 0, True)

        for idx, __url in enumerate(self.chapters[_min:_max], start=_min + 1):
            self.chapter_id = idx - 1
            if dl.already_downloaded():
                info('Skip chapter %d / %s' % (idx, __url))
                continue
            if self._show_chapter_info:
                print('\n\nCurrent chapter url: %s\n' % (self.chapter,), file=stderr)

            count += 1

            chapter_for_json = self.chapter_for_json()

            chapter = chapter_for_json if chapter_for_json is not None else self.chapter

            _path = '%s.%s' % self.get_archive_path()

            self._info.add_volume(chapter, _path)

            if not self._simulate:
                self.before_download_chapter()
                dl.volume = chapter
                dl.download_chapter(self.chapter, self.get_archive_path())
                self.after_download_chapter()

            if callable(self.global_progress):
                self.global_progress(self.chapters_count, idx - _min)
            info('Processed chapter %d / %s' % (idx, __url))

            self._wait_after_chapter()

        for idx, __url in enumerate(self.chapters[_max:], start=_max + 1):
            info('Skip chapter %d / %s' % (idx, __url))

        if count == 0 and not self.quiet:
            print('No new chapters found', file=stderr)

    def get_archive_path(self) -> Tuple[str, str]:
        if self._override_name:
            _path = "{}_{}".format(self._override_name, str(self.normal_arc_name(self.get_chapter_index().split('-'))))
        else:
            # see Std
            _path = remove_file_query_params(self.get_archive_name())
        _path = self.remove_not_ascii(_path)

        if not _path:
            _path = str(self.chapter_id)

        additional_data_name = ''
        if self.http().has_error:
            additional_data_name = '.ERROR'
            self.http().has_error = False
            warning('Error processing chapter.')

        # Manga online biz use this naming scheme (see http2). Not sure if wanted
        # arc_name =  '{:0>3}-{}'.format(idx, self.get_archive_name())
        # If we want to keep it, maybe instead override self.get_archive_name ?
        arc_name = '%s%s' % (_path, additional_data_name)

        return (
            path_join(
                self._params.get('destination', 'Manga'),
                self.name,
                arc_name
            ).replace('?', '_').replace('"', '_').replace('>', '_').replace('<', '_').replace('|', '_')  # Windows...
            , self._archive_type()
        )

    def html_fromstring(self, url, selector: str = None, idx: int = None):
        params = {}
        if isinstance(url, dict):
            params = url['params']
            url = url['url']
        return self.document_fromstring(self.http_get(url, **params), selector, idx)

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
        return self._params['cookies'] and len(self._params['cookies']) and self._params['user_agent'] and len(
            self._params['user_agent'])

    def update_ua(self, ua):
        self._storage['user_agent'] = ua
        self.http().user_agent = ua
        self._info and self._info.set_ua(ua)

    def update_cookies(self, cookies):
        for k in cookies:
            self._storage['cookies'][k] = cookies[k]
            self.http().cookies[k] = cookies[k]

    def before_download_file(self, idx, url):
        url = self.before_file_save(url, idx)
        filename = remove_file_query_params(basename(url))
        _path = Static.remove_not_ascii(self._image_name(idx, filename))
        _path = get_temp_path(_path)
        return _path, idx, url

    # region specified data for eduhoribe/comic-builder (see https://github.com/manga-py/manga-py/issues/347)

    def chapter_details(self, chapter) -> dict:
        """
        Following the pattern specified in
        https://github.com/eduhoribe/comic-builder/blob/goshujin-sama/samples/chapter-metadata-sample.json
        """
        pass

    def manga_details(self) -> dict:
        """
        Following the pattern specified in
        https://github.com/eduhoribe/comic-builder/blob/goshujin-sama/samples/comic-metadata-sample.json
        """
        pass

    # endregion
