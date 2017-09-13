# Manga-Downloader

## Поддерживаемые ресурсы

Смотрите https://yuru-yuri.github.io/Manga-Downloader/#resources-list


## Как использовать

### Установка

```bash
git clone --progress --prune --recurse-submodules=no origin  https://github.com/yuru-yuri/Manga-Downloader.git
cd Manga-Downloader
git submodule init
git submodule update --recursive --remote
# install requirements
pip3 install -r requirements.txt
cd helpers/cloudflare_scrape
python setup.py install
```

#### Если используется Windows, обязательно к установке: http://landinghub.visualstudio.com/visual-cpp-build-tools
_Если в процессе установки пакета pycrypto возникает ошибка на Windows, смотреть 'https://github.com/sfbahr/PyCrypto-Wheels'_

### Загрузка манги

___:warning:Для использования с сайтами, защищенными cloudflare, необходима установка Node.js___


___:warning:Утилита всегда добавляет к пути имя манги___

___Для переопределения этого поведения можно использовать ключ --no-name___

```bash
# Загрузка в папку ./manga
./manga.py -i -p -u http://manga-url-here/manga-name
# или в указаную папку /manga/destination/path/
./manga.py -i -p -u http://manga-url-here/manga-name -d /manga/destination/path/
# Использование в интерактивном режиме
./manga.py -i -p
# Пропустить первые 3 главы
./manga.py --skip-volumes 3 -u http://manga-url-here/manga-name
# Можно инвертировать порядок загрузки глав (24 -> 1)
./manga.py --reverse-downloading -u http://manga-url-here/manga-name
```

### Помощь

```bash
./manga.py -h
# или
./manga.py --help
```
