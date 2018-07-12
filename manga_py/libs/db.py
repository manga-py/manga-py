import peewee
from .fs import storage
from binascii import crc32


__cache = {}


def _db_cache(path=None) -> peewee.Database:
    if path is None:
        path = storage('manga.db')
    crc = crc32(path.encode())
    if __cache.get(crc, None) is None:
        __cache[crc] = peewee.SqliteDatabase(path)
    return __cache[crc]


class Db:
    class Meta:
        database = _db_cache()

 
class Manga(Db):
    # id = peewee.PrimaryKeyField(primary_key=True)
    id = peewee.UUIDField(primary_key=True)  # sqlite
    url = peewee.CharField(unique=True)
    name = peewee.CharField()
    path = peewee.CharField(max_length=2047)
    files = peewee.CharField(max_length=2047)  # json data
    latest_chapter = peewee.IntegerField()
    created = peewee.DateTimeField(default=peewee.datetime.datetime.now)
    updated = peewee.DateTimeField(default=peewee.datetime.datetime.now)
    data = peewee.TextField()  # cookies, browser, args

    class Meta:
        table_name = 'manga'


def make_db(path=None):
    _db_cache(path).create_tables([Manga], safe=True)
