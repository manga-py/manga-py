from pathlib import Path
from typing import NamedTuple, List, Optional


class FileTuple(NamedTuple):
    idx: int
    paths: List[Path]


class ChapterFilesTuple(NamedTuple):
    image: Optional[str]
    archive: Optional[str]


__all__ = ['FileTuple', 'ChapterFilesTuple']
