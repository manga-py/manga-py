import peewee
from .fs import storage, is_file, unlink
from binascii import crc32


__cache = {}


def _db_path(path) -> str:
    if path is None:
        path = storage('manga.db')
    return str(path)


def _db_cache(path=None) -> peewee.Database:
    path = _db_path(path)
    crc = crc32(path.encode())
    if __cache.get(crc, None) is None:
        __cache[crc] = peewee.SqliteDatabase(path)
    return __cache[crc]


class Manga(peewee.Model):
    url = peewee.CharField(unique=True)
    name = peewee.CharField()
    path = peewee.CharField(max_length=2047)
    active = peewee.BooleanField(default=True)
    latest_chapter = peewee.IntegerField()
    created = peewee.DateTimeField(default=peewee.datetime.datetime.now)
    updated = peewee.DateTimeField(default=peewee.datetime.datetime.now)
    data = peewee.TextField()  # cookies, browser, args. JSON data

    @classmethod
    def update_or_insert(cls, data):
        pass

    class Meta:
        database = _db_cache()
        table_name = 'manga'


def make_db(path=None, force=False):
    path = _db_path(path)
    if force:
        unlink(path)
    if not is_file(path):
        _db_cache(path).create_tables([Manga], safe=True)
