import imghdr
from os import path
from typing import Tuple, Optional

from PIL import Image as PilImage, ImageChops, ImageFile
try:
    from PIL import UnidentifiedImageError
except (ModuleNotFoundError, ImportError):
    UnidentifiedImageError = OSError


__all__ = ['MangaImage']


def _pil_fmt(_) -> Optional[str]:
    try:
        with PilImage.open(_) as img:
            return img.format.lower()
    except UnidentifiedImageError:
        return None


class MangaImage:
    _image = None  # type: PilImage.Image
    src_path = None  # type: str

    def __init__(self, src_path):
        """
        :param src_path:
        """
        if not path.isfile(src_path):
            raise AttributeError('Image not found')

        self.src_path = src_path
        try:
            self._image = PilImage.open(src_path)
        except UnidentifiedImageError:
            if not ImageFile.LOAD_TRUNCATED_IMAGES:
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                self._image = PilImage.open(src_path)

    @staticmethod
    def new(mode: str, size: Tuple[int, int]):
        return PilImage.new(mode, size)

    @property
    def image(self) -> PilImage.Image:
        """
        :rtype: PilImage.Image
        :return:
        """
        return self._image

    @image.setter
    def image(self, image: PilImage.Image):
        self._image = image

    def gray(self, dest_path: str):
        """
        :param dest_path:
        :return:
        """
        try:
            image = self.image.convert('LA')
        except (ValueError, OSError):
            image = self.image.convert('L')
        if dest_path is not None:
            image.save(dest_path)
        return image

    def convert(self, dest_path: str, quality: int = 95):
        """
        see http://pillow.readthedocs.io/en/3.4.x/handbook/image-file-formats.html
        :param dest_path:
        :param quality:
        :return:
        """
        self.image.save(dest_path, quality=quality)
        return dest_path

    def crop_manual_with_offsets(self, offsets, dest_path: str):
        """
        :param offsets:
        :param dest_path:
        :return:
        """
        left, upper, right, lower = offsets
        width, height = self.image.size
        image = self.image.crop((
            left,
            upper,
            width - right,
            height - lower
        ))
        image.save(dest_path)

    def crop_manual(self, sizes: tuple, dest_path: str):
        """
        :param sizes: The crop rectangle, as a (left, upper, right, lower)-tuple.
        :param dest_path:
        :return:
        """
        self.image.crop(sizes).save(dest_path)

    def crop_auto(self, dest_path: str):
        """
        :param dest_path:
        :return:
        """
        bg = PilImage.new(
            self.image.mode,
            self.image.size,
            self.image.getpixel((0, 0))
        )
        diff = ImageChops.difference(self.image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            crop = self.image.crop(bbox)
            if dest_path:
                crop.save(dest_path)

    def close(self):
        self.image is not None and self.image.close()

    @staticmethod
    def real_extension(_path):
        ext = imghdr.what(_path)
        if ext is None:
            ext = _pil_fmt(_path)
        if ext is None:
            return None
        return '.%s' % ext

    @staticmethod
    def is_image(_path) -> bool:
        return (imghdr.what(_path) or _pil_fmt(_path)) is not None
