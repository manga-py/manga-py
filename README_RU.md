# Manga Downloader [![Travis CI result](https://travis-ci.org/yuru-yuri/manga-dl.svg?branch=master)](https://travis-ci.org/yuru-yuri/manga-dl/branches)

## Поддерживаемые ресурсы

Смотрите https://yuru-yuri.github.io/manga-dl/#resources-list


## Как использовать

### Установка

1) Установить python 3.5+
https://www.python.org/downloads/
2) Установить pip пакет:
```bash
pip install manga-py
```
3) Запустить программу:

**\*nix, MacOS:**
```bash
manga-py http://manga.url/manga/name
```
__Windows__

3.1) Нажать < Win+r >

3.2) Ввести __cmd__

3.3) Нажать < Enter >

3.4) Смотрите *nix инструкции

####  Если используется Windows, обязательно к установке: https://www.microsoft.com/en-us/download/details.aspx?id=48159
_Если в процессе установки пакета pycrypto возникает ошибка на Windows, смотреть 'https://github.com/sfbahr/PyCrypto-Wheels'_

### Загрузка манги

___:warning:Для использования с сайтами, защищенными cloudflare, необходима установка Node.js___

___:warning:По умолчанию, изображения скачиваются в мультипоточном режиме___

___Для переопределения этого поведения можно использовать ключ  --no-multi-threads___

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
