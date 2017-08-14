# Manga-Downloader

## Supported sites
- [x] http://desu.me
- [x] http://manga-online.biz
- [x] http://mangaclub.ru
- [x] http://mangago.me
- [x] http://mangahub.ru
- [x] http://mangapanda.com
- [x] http://mangarussia.com
- [x] http://mintmanga.me
- [x] http://ninemanga.com
- [x] http://readmanga.me
- [x] http://selfmanga.ru
- [x] http://shakai.ru
- [x] http://read.yagami.me
- [x] http://yaoichan.me
---

## How to use

### Installation
```bash
git clone --recursive  https://github.com/yuru-yuri/Manga-Downloader.git
cd Manga-Downloader
# install requirements
pip3 -r requirements.txt
cd helpers/cloudflare_scrape
python setup.py install
```
### Downloading
```bash
./manga.py -i -p -u http://manga-url-here/manga-name -d /manga/destination/path/
# or interactive mode
./manga.py -i -p
```
### Help
```bash
./manga.py -h
# or
./manga.py --help
```
