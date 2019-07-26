from binascii import crc32
from datetime import datetime
from pathlib import Path

import peewee

from manga_py.libs.fs import user_path

__cache = {}


def db_path() -> Path:
    """
    Overload this to change the path to the database
    :return:
    """
    return user_path().joinpath('manga.db')


def make_db(force=False):
    path = db_path()
    force and path.unlink()
    if not path.is_file():
        _db_cache().create_tables([Manga], safe=True)


def _db_cache() -> peewee.Database:
    path = db_path()
    crc = crc32(str(path).encode())
    if __cache.get(crc, None) is None:
        __cache[crc] = peewee.SqliteDatabase(path)
    return __cache[crc]


class Manga(peewee.Model):
    key = peewee.CharField(unique=True)
    url = peewee.CharField()
    name = peewee.CharField()
    path = peewee.CharField(max_length=2047)
    active = peewee.BooleanField(default=True)
    created_at = peewee.DateTimeField(default=datetime.now())
    updated_at = peewee.DateTimeField(null=True)
    chapters = peewee.TextField()  # downloaded chapters list. JSON data
    data = peewee.TextField()  # cookies, browser, args. JSON data

    @classmethod
    def update_or_insert(cls, data: dict, key='key'):
        db = cls.get_or_none(getattr(Manga, key) == data.get(key))
        del data['created_at']
        del data[key]
        if db is not None:
            db.update(**data, updated=datetime.now())
            db.save()
        else:
            del data['updated_at']
            db.create(**data)

    class Meta:
        database = _db_cache()
        table_name = 'manga'
