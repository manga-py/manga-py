from os import path

from PIL import Image as PilImage, ImageChops


class Image:

    image = None

    def __init__(self, src_path):
        if not path.isfile(src_path):
            raise AttributeError('Image not found')

        self.src_path = src_path

    def __open(self, _path):
        image = PilImage.open(_path)
        self.image = image
        return image

    def gray(self, dest_path: str = None):
        img = self.__open(self.src_path)
        try:
            image = img.convert('LA')
        except (ValueError, OSError):
            image = img.convert('L')
        if dest_path is not None:
            image.save(dest_path)
        return image

    def convert(self, dest_path: str=None, quality: int = 95):
        """
        see http://pillow.readthedocs.io/en/3.4.x/handbook/image-file-formats.html
        :param dest_path:
        :param quality:
        :return:
        """
        _path = self.src_path
        image = self.__open(_path)
        if not dest_path:
            dest_path = _path
        image.save(dest_path, quality=quality)
        return dest_path

    def crop_manual_with_offsets(self, offsets = None, dest_path: str = None):
        if offsets is None:
            return
        image = self.__open(self.src_path)
        if dest_path is None:
            dest_path = self.src_path
        left, upper, right, lower = offsets
        width, height = image.size
        image = image.crop((
            left,
            upper,
            width - right,
            height - lower
        ))
        self.transparency_fixed_before_save(image, dest_path).save(dest_path)

    def crop_manual(self, sizes: tuple = None, dest_path: str = None):
        """
        :param sizes: The crop rectangle, as a (left, upper, right, lower)-tuple.
        :param dest_path:
        :return:
        """
        if sizes is None:
            return
        image = self.__open(self.src_path)
        image = image.crop(sizes)
        if dest_path is None:
            dest_path = self.src_path
        _ = self.transparency_fixed_before_save(image, dest_path)
        _.save(dest_path)
        _.close()

    def crop_auto(self, dest_path: str = None):
        image = self.__open(self.src_path)
        bg = PilImage.new(image.mode, image.size, image.getpixel((0, 0)))
        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            crop = image.crop(bbox)
            if dest_path:
                crop.save(dest_path)
                crop.close()
            return crop

    @staticmethod
    def transparency_fixed_before_save(image: PilImage, _path: str) -> PilImage:
        ext = _path[_path.rfind('.'):]
        if ext not in ['.png', '.webp']:
            return image.convert('RGB')
        return image

    def close(self):
        self.image and self.image.close()
