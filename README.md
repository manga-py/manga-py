# Manga-Downloader
[![Code Climate](https://codeclimate.com/github/yuru-yuri/Manga-Downloader/badges/gpa.svg)](https://codeclimate.com/github/yuru-yuri/Manga-Downloader)
[![Test Coverage](https://codeclimate.com/github/yuru-yuri/Manga-Downloader/badges/coverage.svg)](https://codeclimate.com/github/yuru-yuri/Manga-Downloader/coverage)
[![Issue Count](https://codeclimate.com/github/yuru-yuri/Manga-Downloader/badges/issue_count.svg)](https://codeclimate.com/github/yuru-yuri/Manga-Downloader)
[![Travis CI result](https://travis-ci.org/yuru-yuri/Manga-Downloader.svg?branch=master)](https://travis-ci.org/yuru-yuri/Manga-Downloader)
 
[![GitHub issues](https://img.shields.io/github/issues/yuru-yuri/Manga-Downloader.svg)](https://github.com/yuru-yuri/Manga-Downloader/issues)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/yuru-yuri/Manga-Downloader/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yuru-yuri/Manga-Downloader.svg)](https://github.com/yuru-yuri/Manga-Downloader/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yuru-yuri/Manga-Downloader.svg)](https://github.com/yuru-yuri/Manga-Downloader/network)

## Supported resources

see https://yuru-yuri.github.io/Manga-Downloader/#resources-list


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
