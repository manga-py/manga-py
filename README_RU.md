# Manga Downloader [![Travis CI result](https://travis-ci.org/yuru-yuri/manga-dl.svg?branch=master)](https://travis-ci.org/yuru-yuri/manga-dl/branches)

## Поддерживаемые ресурсы

Смотрите https://yuru-yuri.github.io/manga-dl/#resources-list


## Как использовать

### Установка

1) Установить python 3.5+ https://www.anaconda.com/downloads
2) Установить pip пакет:
```bash
pip install manga-py
```
3) Запустить программу:

```bash
manga-py http://manga.url/manga/name
```

```bash
# Загрузка в папку "./Manga"
manga-py http://manga-url-here/manga-name
# Загрузка в папку "./Manga Name"
manga-py http://manga-url-here/manga-name --name 'Manga Name'
# или в указаную папку /manga/destination/path/
manga-py http://manga-url-here/manga-name -d /manga/destination/path/
# Пропустить первые 3 главы
manga-py --skip-volumes 3 http://manga-url-here/manga-name
# Пропустить первые 3 главы и загрузить 2
manga-py --skip-volumes 3 --max-volumes 2 http://manga-url-here/manga-name
# Можно инвертировать порядок загрузки глав (24 -> 1)
manga-py --reverse-downloading http://manga-url-here/manga-name
```

### Помощь

```bash
manga-py -h
# или
manga-py --help
```
