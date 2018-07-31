import peewee
from .fs import storage, is_file, unlink
from binascii import crc32
from datetime import datetime


__cache = {}


def db_path() -> str:
    """
    Overload this to change the path to the database
    :return:
    """
    return storage('manga.db')


def _db_cache() -> peewee.Database:
    path = db_path()
    crc = crc32(path.encode())
    if __cache.get(crc, None) is None:
        __cache[crc] = peewee.SqliteDatabase(path)
    return __cache[crc]


class Manga(peewee.Model):
    key = peewee.CharField(unique=True)
    url = peewee.CharField()
    name = peewee.CharField()
    path = peewee.CharField(max_length=2047)
    active = peewee.BooleanField(default=True)
    latest_chapter = peewee.IntegerField()
    created = peewee.DateTimeField(default=datetime.now())
    updated = peewee.DateTimeField(default=datetime.now())
    data = peewee.TextField()  # cookies, browser, args. JSON data

    @classmethod
    def update_or_insert(cls, data: dict, key='key'):
        db = cls.get_or_none(getattr(Manga, key) == data.get(key))
        if db is not None:
            db.update(**data, updated=datetime.now())
            db.save()
        else:
            db.create(**data)

    class Meta:
        database = _db_cache()
        table_name = 'manga'


def make_db(force=False):
    path = db_path()
    force and unlink(path)
    if not is_file(path):
        _db_cache().create_tables([Manga], safe=True)
