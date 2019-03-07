from argparse import ArgumentParser, Namespace
from sys import stderr
from typing import List

from tabulate import tabulate

from manga_py.libs import print_lib
from manga_py.libs.db import Manga, make_db


def args():
    args_parser = ArgumentParser()
    args_parser.add_argument('idx', type=str, help='Get manga info from ids', nargs="*")
    args_parser.add_argument('--list', action='store_const', const=True,
                             help='Show all manga', default=False)
    args_parser.add_argument('-f', '--filter', metavar='name', type=str, help='Filter manga from name')
    args_parser.add_argument('-d', '--disable', metavar='id', type=int,
                             help='Disable manga (see manga ids from --list/filter)', default=0)
    args_parser.add_argument('-e', '--enable', metavar='id', type=int,
                             help='Enable manga (see manga ids from --list/filter)', default=0)
    args_parser.add_argument('--delete', metavar='id', type=int,
                             help='Delete manga (see manga ids from --list/filter)', default=0)
    args_parser.add_argument('--delete-all', action='store_const', const=True,
                             help='WARNING! Delete all manga from database', default=False)

    return args_parser.parse_args()


class DataBase:
    _db = None  # type: Manga

    def __init__(self):
        make_db()
        self._db = Manga

    def run(self, args: Namespace):
        if len(args.idx):
            self.print_from_idx(*args.idx)
        else:
            (args.list or args.filter) and self.print_all(args.filter)
            args.enable and self.enable(args.enable)
            args.disable and self.disable(args.disable)
            args.delete and self.delete(args.delete)
            args.delete_all and self.clean()

    def enable(self, idx: int):
        col = self.get_one(idx)
        if col:
            col.update(active=True)
            if col.save():
                print_lib('Enabled manga <%d>' % idx, file=stderr)
        else:
            print_lib('Id <%d> not found' % idx, file=stderr)

    def disable(self, idx: int):
        col = self.get_one(idx)
        if col:
            col.update(active=False)
            if col.save():
                print_lib('Updated manga <%d>' % idx, file=stderr)
        else:
            print_lib('Id <%d> not found' % idx, file=stderr)

    def delete(self, idx: int):
        col = self.get_one(idx)
        if col:
            col.update(active=False)
            if col.save():
                print_lib('Deleted manga <%d>' % idx, file=stderr)
        else:
            print_lib('Id <%d> not found' % idx, file=stderr)

    def clean(self):
        make_db(force=True)
        print_lib('Database clean now!', file=stderr)

    def get_one(self, idx: int) -> Manga:
        return self._db.get_or_none(self._db.id == idx)

    def print_from_idx(self, *idx: int):
        data = []
        headers = ['id', 'name', 'active', 'path', 'created', 'updated']
        for _idx in idx:
            col = self.get_one(_idx)
            if col:
                data.append([
                    col.id,
                    col.name,
                    col.active,
                    col.path,
                    col.created,
                    col.updated,
                ])
        if len(data) > 0:
            print_lib(tabulate(data, headers))
        else:
            print_lib('Database is empty')

    def get_all(self, *fields, _filter: str = None) -> List[Manga]:
        if _filter:
            pass
        return self._db.select(*fields)

    def print_all(self, _filter: str):
        headers = ['id', 'name', 'active', 'path', 'created', 'updated']
        data = []
        for col in self.get_all():
            data.append([
                col.id,
                col.name,
                col.active,
                col.path,
                col.created,
                col.updated,
            ])
        if len(data) > 0:
            print_lib(tabulate(data, headers))
        else:
            print_lib('Database is empty')

    def get_db(self) -> Manga:
        if not isinstance(self._db, Manga):
            AttributeError('DB class not init')
        return self._db
