import peewee
from .fs import storage
from binascii import crc32


__cache = {}


def _db_cache(path=None) -> peewee.Database:
    if path is None:
        path = storage('manga.db')
    crc = crc32(path.encode())
    __db = __cache.get(crc, None)
    if __db is not None:
        return __db
    else:
        __cache[crc] = peewee.SqliteDatabase(path)
    return __cache[crc]


class Db:
    class Meta:
        database = _db_cache()

 
class Manga(Db):
    id = peewee.PrimaryKeyField(primary_key=True)
    url = peewee.CharField(unique=True)
    name = peewee.CharField()
    path = peewee.CharField(max_length=2047)
    files = peewee.CharField(max_length=2047)  # json data
    latest_chapter = peewee.IntegerField()
    created = peewee.DateTimeField(default=peewee.datetime.datetime.now)
    updated = peewee.DateTimeField(default=peewee.datetime.datetime.now)

    class Meta:
        table_name = 'manga'


# class Cookies(Db):
#     id = peewee.PrimaryKeyField(primary_key=True)
#     domain = peewee.CharField()
#     key = peewee.CharField()
#     value = peewee.CharField()
#     expires = peewee.IntegerField()
#
#     class Meta:
#         table_name = 'cookies'


def make_db(path=None):
    _db_cache(path).create_tables([Manga], safe=True)
