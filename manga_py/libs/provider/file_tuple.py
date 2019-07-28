from pathlib import Path
from typing import NamedTuple, List, Optional

TYPE_IMAGE = 0
TYPE_ARCHIVE = 1

try:
    # files tuple after download
    class FileTuple(NamedTuple):
        idx: str
        paths: List[Path]
        type: int
except TypeError:
    NamedTuple('FileTuple', [('idx', str), ('paths', List[Path]), ('type', int)])


try:
    # chapter tuple
    class ChapterTuple(NamedTuple):
        idx: str
        url: str
except TypeError:
    NamedTuple('ChapterTuple', [('idx', str), ('url', str)])


try:
    # files to archive
    class ChapterFilesTuple(NamedTuple):
        images: Optional[List[str]]
        archive: Optional[str]
except TypeError:
    NamedTuple('ChapterFilesTuple', [('images', Optional[List[str]]), ('archive', Optional[str])])


__all__ = ['FileTuple', 'ChapterTuple', 'ChapterFilesTuple', 'TYPE_ARCHIVE', 'TYPE_IMAGE']
