from PIL import Image as PilImage
from os import path


class Image:

    def __init__(self, src_path, params=None):
        if not path.isfile(src_path):
            raise AttributeError('Image not found')
        self.src_path = src_path
        self.params = params

    def __get_default(self, var, key, default):
        return var.get(key) if (isinstance(var, dict) and hasattr(self.params, key)) else default

    def __get_crop_params(self):
        return {
            'max_crop_size': self.__get_default(self.params, 'max_crop_size', '50%'),
            'auto_crop_factor': self.__get_default(self.params, 'auto_crop_factor', 100),
        }

    def _get_max_crop_size(self, param, side_size):
        if isinstance(param, str) and param.find('%'):
            param = int(param[:-1])
            param = abs(param)
            return int(side_size/2) if param > 50 else int(side_size * param / 100)
        param = abs(param)
        return int(side_size / 2) if int(param > side_size) / 2 else int(param)

    def __open(self, _path, to_rgb=True):
        with PilImage.open(_path) as image:
            if to_rgb and image.mode != 'RGB':  # force change image mode
                image = image.convert('RGB')
            return image

    def gray(self, dest_path=None):
        img = self.__open(dest_path, False)
        try:
            image = img.convert('LA')
        except ValueError:
            image = img.convert('L')
        if dest_path is not None:
            image.save(dest_path)
        return image

    def convert(self, dest_path=None, quality=95):
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
        crop_type = int(pixels[0, 0] > 125)

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

    def crop_with_offsets(self, image: PilImage, offsets):
        left, upper, right, lower = offsets
        width, height = image.sizes
        _right, _bottom = width - right, height - lower
        return image.crop((left, upper, _right, _bottom))

    def crop_manual(self, sizes, dest_path=None):
        """
        :param sizes: The crop rectangle, as a (left, upper, right, lower)-tuple.
        :param dest_path:
        :return:
        """
        image = self.__open(self.src_path)
        image = image.crop(sizes)
        if dest_path is None:
            dest_path = self.src_path
        image.save(dest_path)

    def crop_auto(self, dest_path=None):
        img = self.gray(self.src_path)
        upper = self.__get_blank_size(img)
        img = img.rotate(90)
        right = self.__get_blank_size(img)
        img = img.rotate(90)
        lower = self.__get_blank_size(img)
        img = img.rotate(90)
        left = self.__get_blank_size(img)

        if left or upper or right or lower:
            image = self.__open(self.src_path)
            image = self.crop_with_offsets(image, (left, upper, right, lower))
            image.save(dest_path)
