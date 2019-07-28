from typing import Optional
from PIL import Image
from pathlib import Path


class Img:
    _path = None  # type: Path
    _image = None  # type: Image.Image

    def __init__(self, path: Path):
        self._path = path
        self._image = Image.open(path)

    @property
    def format(self) -> Optional[str]:
        return self._image.format

    def path_with_real_format(self) -> Path:
        suffix = self.format or '.png'
        without_ext = str(self._path)[:(-1 * len(self._path.suffix))]
        if suffix != self._path.suffix:
            _path = '{}{}'.format(without_ext, suffix)
            return Path(_path)
        return self._path


__all__ = ['Img']
