#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import (get as get_request, post as post_request)
import lxml.html as html
import zipfile
from urllib import (
    request as url_request,
    error as url_error,
    parse
)
import tempfile
import os
import random
import re
import json
from sys import stderr
from shutil import (rmtree, move)

domainUri = 'http://shakai.ru'
uriRegex = 'https?://(?:www\.)?shakai\.ru/manga(?:-read)?/(\d+)/?'
# imagesDirRegex = 'servers\s?=\s?"(.*)"'
imagesRegex = 'rm_h\.init.+?(\[\[.+\]\])'
archivesDir = os.path.join(os.getcwd(), 'manga')

rnd_temp_path = str(random.random())


if not os.path.isdir(archivesDir):
    if not os.access(os.getcwd(), os.W_OK):
        print('Current directory not writeable and manga directory not exist', file=stderr)
        exit(1)
    os.makedirs(archivesDir)
elif not os.access(archivesDir, os.W_OK):
    print('Manga directory not writable', file=stderr)
    exit(1)


def _get(filename: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None):
    if not headers:
        headers = {}
    if not cookies:
        cookies = ()
    response = get_request(filename, headers=headers, cookies=cookies)
    ret = response.text
    if offset > 0:
        ret = ret[offset:]
    if maxlen > 0:
        ret = ret[:maxlen]
    return ret


def _post(filename: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None, data: dict = ()):
    if not headers:
        headers = {}
    if not cookies:
        cookies = ()
    response = post_request(filename, headers=headers, cookies=cookies, data=data)
    ret = response.text
    if offset > 0:
        ret = ret[offset:]
    if maxlen > 0:
        ret = ret[:maxlen]
    return ret


def _safe_downloader(url, file_name):
    try:
        response = url_request.urlopen(url)
        out_file = open(file_name, 'wb')
        out_file.write(response.read())
        return True
    except url_error.HTTPError:
        return False
    except url_error.URLError:
        return False


def get_temp_path(path: str = ''):
    rnd_dir = os.path.join(tempfile.gettempdir(), rnd_temp_path)
    if not os.path.isdir(rnd_dir):
        os.makedirs(rnd_dir)
    return os.path.join(rnd_dir, path)


def get_content(uri: str):
    """
    :param uri:
    :return:
    """
    result = _get(uri)
    if result is None:
        return b''
    return result


def download_files(images, archive_name: str, subfolder: str = ''):
    temp_directory = get_temp_path()
    if os.path.isdir(temp_directory):
        rmtree(temp_directory)
    os.makedirs(temp_directory)
    images_count = len(images)
    i = 0

    archive_folder = os.path.join(archivesDir, subfolder, archive_name)
    archive = archive_folder + '.zip'

    if os.path.isfile(archive):
        print('Archive ' + archive + ' exist. Skip')
        return

    create_archive = True

    _dirname = os.path.dirname(archive)
    if not os.path.isdir(_dirname):
        os.makedirs(_dirname)

    print('Images count:', images_count)

    while i < images_count:
        _url = images[i]
        name = os.path.basename(_url)
        _url = parse.quote(_url, '/:?')
        i += 1

        if not _safe_downloader(_url, os.path.join(temp_directory, name)):
            print('Warning! Don\'t downloaded file. Retry')
            if not _safe_downloader(_url, os.path.join(temp_directory, name)):
                print('Error downloading %s' % _url, file=stderr)
                create_archive = False
                # return

    if create_archive:
        archive = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)

        for f in os.listdir(temp_directory):
            file = os.path.join(temp_directory, f)
            if os.path.isfile(file):
                archive.write(file, f)
        archive.close()
    else:
        if os.path.isdir(archive_folder):
            print('Please, move files manually and press enter (src: %s dst: %s' % (temp_directory, archive_folder, ))
            input()
        else:
            move(temp_directory, archive_folder)


def get_volumes_links(content: str):
    """
    :param content: str
    :return: dict
    """
    parser = html.document_fromstring(content)
    result = parser.cssselect('#mangaBox > div.leftContent div.chapters-link tr > td > a')
    if result is None:
        return []
    return [i.get('href') for i in result]


def get_manga_name(url):
    result = re.match(uriRegex, url)
    if result is None:
        return ''
    result = result.groups()
    if not len(result):
        return ''
    return result[0]


def main():
    print('Please, paste shakai.ru manga url.')
    print('Example: http://shakai.ru/manga/123/')
    url = str(input())
    # url = 'http://shakai.ru/manga/123'
    name = get_manga_name(url)

    if not len(name):
        print('Error url. Exit', file=stderr)
        exit(1)

    print('Start downloading manga %s' % (name))

    _ = {
        'dataRun': 'api-manga',
        'dataRequest': name
    }
    page_content = json.loads(str(_post('http://shakai.ru/take/api-manga/request/shakai', data=_)))

    if page_content is None or 'data' not in page_content:
        print('Response error', file=stderr)
        exit(1)

    volumes_links = page_content['data']
    volumes_count = len(volumes_links)

    if volumes_count < 1:
        print('Volumes not found. Exit', file=stderr)
        exit(1)

    print('Volumes count: %d' % volumes_count)
    loop = 0
    while loop < volumes_count:
        print('Start downloading volume %d' % (loop+1))
        data = volumes_links[loop]
        loop += 1
        archive_name = name + '_' + data['data-first']
        images = data['data-second']
        if images is None:
            print('Warning get images list')
            continue
        download_files(images, archive_name, 'shakai_' + name)


if __name__ == '__main__':
    main()
    rmtree(get_temp_path())
