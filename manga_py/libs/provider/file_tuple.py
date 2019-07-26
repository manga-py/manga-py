from pathlib import Path
from typing import NamedTuple, List, Optional


try:
    class FileTuple(NamedTuple):
        idx: int
        paths: List[Path]
except TypeError:
    NamedTuple('FileTuple', [('idx', int), ('paths', List[Path])])


try:
    class ChapterFilesTuple(NamedTuple):
        image: Optional[str]
        archive: Optional[str]
except TypeError:
    NamedTuple('FileTuple', [('idx', int), ('paths', List[Path])])


__all__ = ['FileTuple', 'ChapterFilesTuple']
