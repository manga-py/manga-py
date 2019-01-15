from PIL import Image as PilImage, ImageChops
import imghdr
from pathlib import PurePath
from typing import Union


class Image:
    _image = None
    _format = None

    def __init__(self, image: Union[str, PilImage.Image]):
        if isinstance(image, str):
            self._image = PilImage.open(image)
        elif isinstance(image, PilImage.Image):
            self._image = image

    def __add__(self, other):
        margin = 5
        size = self._image.size
        other_size = other.size
        if (
            size[0] < (other_size[0] + 2 * margin) or
            size[1] < (other_size[1] + 2 * margin)
        ):
            other_size = (size[0] - margin*2, size[1] - margin*2)
            other.resize(other_size, PilImage.ANTIALIAS)
        self._image.paste(other, (margin, margin))

    def set_out_format(self, format: str):
        """
        https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html
        :param format:
        :return:
        """
        self._format = format

    def save(self, fp, **kwargs):
        if self._format is not None and isinstance(fp, (str, PurePath)):
            fp = PurePath(str(fp)).with_suffix('.' + self._format)
        self._image.save(fp, format=self._format, **kwargs)

    def calc_sides(self, need, inside=True) -> PilImage:
        image = self._image.copy()
        orig = image.size
        if inside:
            scale = max(*orig) / max(*need)
        else:
            scale = min(*orig) / min(*need)
        return image.resize((scale * need[0], scale * need[1]), PilImage.ANTIALIAS)

    def auto_crop(self):
        bg = PilImage.new(
            self._image.mode,
            self._image.size,
            self._image.getpixel((1, 1))
        )
        diff = ImageChops.difference(self._image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        diff.close()
        return self._image.crop(bbox)

    def auto_split(self):  # TODO
        pass

    def manual_crop(self, top: int = 0, right: int = 0, bottom: int = 0, left: int = 0):
        """
        Relative sizes!
        :param int top:
        :param int right:
        :param int bottom:
        :param int left:
        :return:
        """
        sides = top, right, bottom, left
        return self._image.crop(sides)

    def grayscale(self):
        return self._image.convert('LA')

    @classmethod
    def process(cls, file, args: dict):
        """
        :param file:
        :param args:
        :type file File
        :return:
        """
        _orig = True
        img = cls(file.path_location)

        # 'crop-blank'
        if args['crop_blank']:
            _orig = False
            img.auto_crop()

        if args['Xt'] > 0 or args['Xr'] > 0 or args['Xb'] > 0 or args['Xl'] > 0:
            _orig = False
            img.manual_crop(
                args['Xt'],
                args['Xr'],
                args['Xb'],
                args['Xl'],
            )

        if args['jpg']:
            _orig = False
            img.format = 'jpg'
        elif args['png']:
            _orig = False
            img.format = 'png'

        if _orig:
            return None
        return img

    @classmethod
    def real_extension(cls, path):
        ext = imghdr.what(path)
        if ext:
            ext = '.' + ext
        return ext
