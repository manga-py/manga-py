# Manga-Downloader [![Travis CI result](https://travis-ci.org/yuru-yuri/manga-dl.svg?branch=master)](https://travis-ci.org/yuru-yuri/manga-dl)

Universal assistant download manga.<br/>
Supports more than 70 different resources now.<br>

[![Code Climate](https://codeclimate.com/github/yuru-yuri/manga-dl/badges/gpa.svg)](https://codeclimate.com/github/yuru-yuri/manga-dl)
[![Issue Count](https://codeclimate.com/github/yuru-yuri/manga-dl/badges/issue_count.svg)](https://codeclimate.com/github/yuru-yuri/manga-dl)<br/>
[![Scrutinizer CI result](https://scrutinizer-ci.com/g/yuru-yuri/manga-dl/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/yuru-yuri/manga-dl)
[![Scrutinizer CI coverage](https://scrutinizer-ci.com/g/yuru-yuri/manga-dl/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/yuru-yuri/manga-dl)
[![GitHub issues](https://img.shields.io/github/issues/yuru-yuri/manga-dl.svg)](https://github.com/yuru-yuri/manga-dl/issues)<br/>

## Supported resources

see https://yuru-yuri.github.io/manga-dl/#resources-list


## Plans for improvement:

see https://yuru-yuri.github.io/manga-dl/improvement.html

## How to use

### Simple use:
Download executable file from https://github.com/yuru-yuri/manga-dl/releases/latest

### Installation

```bash
git clone --progress --prune --recurse-submodules=no origin  https://github.com/yuru-yuri/manga-dl.git
cd manga-dl
# install requirements
pip3 install -r requirements.txt
```

#### Or alternative installation:
1) Downloading repo: https://github.com/yuru-yuri/manga-dl/releases/latest
2) Extract archive
3) Install requirements
```bash
cd manga-dl
pip3 install -r requirements.txt
```

#### If you using windows, require http://landinghub.visualstudio.com/visual-cpp-build-tools

### Downloading manga

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
cd manga-dl
docker build -t MangaDownloader . # build a docker image
docker run -v /path/to/store/mangas:/app/Manga MangaDownloader ./manga.py -i -p -u http://manga-url-here/manga-name # run it
```
