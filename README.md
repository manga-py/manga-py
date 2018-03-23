# Manga-Downloader [![Travis CI result](https://travis-ci.org/yuru-yuri/manga-dl.svg?branch=master)](https://travis-ci.org/yuru-yuri/manga-dl/branches)

##### Universal assistant download manga.
##### Supports more than 220 resources now.

[![Code Climate](https://codeclimate.com/github/yuru-yuri/manga-dl/badges/gpa.svg)](https://codeclimate.com/github/yuru-yuri/manga-dl)
[![Issue Count](https://codeclimate.com/github/yuru-yuri/manga-dl/badges/issue_count.svg)](https://codeclimate.com/github/yuru-yuri/manga-dl)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/manga-py.svg)](https://pypi.org/project/manga-py/)

[![Scrutinizer CI result](https://scrutinizer-ci.com/g/yuru-yuri/manga-dl/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/yuru-yuri/manga-dl)
[![Scrutinizer CI coverage](https://scrutinizer-ci.com/g/yuru-yuri/manga-dl/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/yuru-yuri/manga-dl)
[![GitHub issues](https://img.shields.io/github/issues/yuru-yuri/manga-dl.svg)](https://github.com/yuru-yuri/manga-dl/issues)


## Supported resources

see https://yuru-yuri.github.io/manga-dl/#resources-list


## Plans for improvement:

see https://yuru-yuri.github.io/manga-dl/improvement.html

## How to use

### Installation

1) Download python 3.5+
https://www.python.org/downloads/
2) Install pip package:
```bash
pip install manga-py
```
3) Run program:

__*nix, MacOS:__
```bash
manga-py  # gui mode (Not worked now. In develop)
manga-py -- cli http://manga.url/manga/name  # For download manga
```
__Windows__

3.1) Press < Win+r >

3.2) Enter __cmd__

3.2.1) _Gui in develop_

3.3) Press < Enter >

3.4) See *nix instruction


#### If you using windows, require http://landinghub.visualstudio.com/visual-cpp-build-tools

### Downloading manga

___:warning:For sites with cloudflare protect need installed Node.js___

___:warning:Notice! By default, the mode of multithreaded image loading is enabled___

___To change this behavior, add the key --no-multi-threads___

```bash
# download to "./Manga" directory
manga-py http://manga-url-here/manga-name
# download to "./Manga Name" directory
manga-py http://manga-url-here/manga-name --name 'Manga Name'
# or download to /manga/destination/path/ directory
manga-py http://manga-url-here/manga-name -d /manga/destination/path/
# skip 3 volumes
manga-py --skip-volumes 3 http://manga-url-here/manga-name
# skip 3 volumes and download 2 volumes
manga-py --skip-volumes 3 --max-volumes 2 http://manga-url-here/manga-name
# reverse volumes downloading (24 -> 1)
manga-py --reverse-downloading http://manga-url-here/manga-name
manga-py --no-progress http://manga-url-here/manga-name  # Disable progressbar
```

### Help

```bash
manga-py -h
# or
manga-py --help
```

### Docker

```bash
cd manga-dl
docker build -t MangaDownloader . # build a docker image
docker run -v /path/to/store/mangas:/app/Manga MangaDownloader ./manga.py --cli http://manga-url-here/manga-name # run it
```
