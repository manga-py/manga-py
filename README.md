# Manga-Downloader [![Travis CI result](https://travis-ci.org/yuru-yuri/Manga-Downloader.svg?branch=master)](https://travis-ci.org/yuru-yuri/Manga-Downloader)

Universal assistant download manga.<br/>
Supports more than 60 different resources now.

## Supported resources

see https://yuru-yuri.github.io/Manga-Downloader/#resources-list


## Plans for improvement:

see https://yuru-yuri.github.io/Manga-Downloader/improvement.html

## How to use

### Installation

```bash
git clone --progress --prune --recurse-submodules=no origin  https://github.com/yuru-yuri/Manga-Downloader.git
cd Manga-Downloader
# install requirements
pip3 install -r requirements.txt
```

#### Or alternative installation:
1) Downloading repo: https://github.com/yuru-yuri/Manga-Downloader/archive/master.zip
2) Extract archive
3) Install requirements
```bash
cd Manga-Downloader
pip3 install -r requirements.txt
```

_If you use Windows, see 'https://github.com/sfbahr/PyCrypto-Wheels'_

#### If you using windows, require http://landinghub.visualstudio.com/visual-cpp-build-tools

### Downloading

___:warning:For sites with cloudflare protect need installed Node.js___


___:warning:Notice! By default, the mode of multithreaded image loading is enabled___

___To change this behavior, add the key --no-multi-threads___


___:warning:Notice! The name of the manga is always added to the path!___

___To change this behavior, add the key --no-name___

```bash
# download to ./manga directory
./manga.py -i -p -u http://manga-url-here/manga-name
# or download to /manga/destination/path/ directory
./manga.py -i -p -u http://manga-url-here/manga-name -d /manga/destination/path/
# or interactive mode
./manga.py -i -p
# skip 3 volumes
./manga.py --skip-volumes 3 -u http://manga-url-here/manga-name
# reverse volumes downloading (24 -> 1)
./manga.py --reverse-downloading -u http://manga-url-here/manga-name
```

### Help

```bash
./manga.py -h
# or
./manga.py --help
```

### Docker

```bash
cd Manga-Downloader
docker build -t MangaDownloader . # build a docker image
docker run -v /path/to/store/mangas:/app/Manga MangaDownloader ./manga.py -i -p -u http://manga-url-here/manga-name # run it
```

[![Code Climate](https://codeclimate.com/github/yuru-yuri/Manga-Downloader/badges/gpa.svg)](https://codeclimate.com/github/yuru-yuri/Manga-Downloader)
[![Issue Count](https://codeclimate.com/github/yuru-yuri/Manga-Downloader/badges/issue_count.svg)](https://codeclimate.com/github/yuru-yuri/Manga-Downloader)<br/>
[![Scrutinizer CI result](https://scrutinizer-ci.com/g/yuru-yuri/Manga-Downloader/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/yuru-yuri/Manga-Downloader)
[![Scrutinizer CI coverage](https://scrutinizer-ci.com/g/yuru-yuri/Manga-Downloader/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/yuru-yuri/Manga-Downloader)
[![GitHub issues](https://img.shields.io/github/issues/yuru-yuri/Manga-Downloader.svg)](https://github.com/yuru-yuri/Manga-Downloader/issues)<br/>
