from pathlib import Path
from typing import NamedTuple, List, Optional

try:
    class FileTuple(NamedTuple):
        idx: int
        paths: List[Path]

    class ChapterFilesTuple(NamedTuple):
        image: Optional[str]
        archive: Optional[str]

except Exception:
    # for Python 3.5 support
    from collections import namedtuple
    FileTuple = namedtuple('FileTuple', ['idx', 'paths'])
    ChapterFilesTuple = namedtuple('ChapterFilesTuple', ['image', 'archive'])

__all__ = ['FileTuple', 'ChapterFilesTuple']
