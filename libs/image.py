from os import path

from PIL import Image as PilImage


class Image:

    image = None

    def __init__(self, src_path, params=None):
        if not path.isfile(src_path):
            raise AttributeError('Image not found')
        params = params if isinstance(params, dict) else {}

        self.src_path = src_path
        self.params = params

    def __get_default(self, var, key, default):
        if isinstance(var, dict):
            return self.params.get(key, default)
        return default

    def __get_crop_params(self):
        return {
            'max_crop_size': self.__get_default(self.params, 'max_crop_size', '50%'),
            'auto_crop_factor': self.__get_default(self.params, 'auto_crop_factor', 100),
        }

    def _get_max_crop_size(self, param, side_size: int):
        if isinstance(param, str) and param.find('%'):
            param = int(param[:-1])
            param = abs(param)
            return int((side_size-1)/2) if param >= 50 else int(side_size * param / 100)
        param = abs(param)
        return int(side_size / 2) if int(param) > (side_size / 2) else int(param)

    def __open(self, _path, to_rgb=True):
        image = PilImage.open(_path)
        if to_rgb and image.mode != 'RGB':  # force change image mode
            image = image.convert('RGB')
        self.image = image
        return image

    def gray(self, dest_path: str = None):
        img = self.__open(self.src_path, False)
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
        try:
            image = self.__open(_path)
            if not dest_path:
                dest_path = '{}.{}'.format(_path[:_path.rfind('.')], _path[_path.frind('.')])
            image.save(dest_path, quality=quality)
            return dest_path
        except OSError:
            return False

    def __get_blank_size(self, img: PilImage):  # TOP ONLY!
        width, height = img.size

        if width < 100 or height < 100:
            return 0

        crop_params = self.__get_crop_params()
        max_offset = self._get_max_crop_size(crop_params.get('max_crop_size'), height)
        factor = crop_params.get('auto_crop_factor')
        pixels = img.load()
        crop_type = int(pixels[0, 0] > 125)  # TODO!

        for h in range(int(height/2) - 1):
            if h > max_offset:
                return h - 1

            for w in range(int(width/2) - 1):
                data = pixels[w*2, h*2]
                condition1 = crop_type and data[0] < factor  # white
                condition2 = not crop_type and data[0] > factor  # black
                if condition1 or condition2:
                    return h - 1

        return 0

    def _crop_with_offsets(self, image: PilImage, offsets: tuple) -> PilImage:
        left, upper, right, lower = offsets
        width, height = image.sizes
        _right, _bottom = width - right, height - lower
        return image.crop((left, upper, _right, _bottom))

    def crop_manual_with_offsets(self, offsets, dest_path: str = None):
        image = self.__open(self.src_path)
        if dest_path is None:
            dest_path = self.src_path
        image = self._crop_with_offsets(image, offsets)
        self.transparency_fixed_before_save(image, dest_path).save(dest_path)

    def crop_manual(self, sizes: tuple, dest_path: str = None):
        """
        :param sizes: The crop rectangle, as a (left, upper, right, lower)-tuple.
        :param dest_path:
        :return:
        """
        image = self.__open(self.src_path)
        image = image.crop(sizes)
        if dest_path is None:
            dest_path = self.src_path
        self.transparency_fixed_before_save(image, dest_path).save(dest_path)

    def crop_auto(self, dest_path: str = None):
        img = self.gray()
        upper = self.__get_blank_size(img)
        img = img.rotate(90)
        right = self.__get_blank_size(img)
        img = img.rotate(90)
        lower = self.__get_blank_size(img)
        img = img.rotate(90)
        left = self.__get_blank_size(img)
        img.close()

        if left or upper or right or lower:
            image = self.__open(self.src_path)
            image = self._crop_with_offsets(image, (left, upper, right, lower))
            self.transparency_fixed_before_save(image, dest_path).save(dest_path)

    def get_ext(self, _path: str):
        return _path[_path.rfind('.'):]

    def transparency_fixed_before_save(self, image: PilImage, _path: str) -> PilImage:
        ext = self.get_ext(_path)
        if ext not in ['.png', '.webp']:
            return image.convert('RGB')
        return image

    def close(self):
        self.image and self.image.close()
