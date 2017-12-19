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
            return 50 if param > 50 else param
        return int(side_size / 2) if int(param > side_size) / 2 else int(param)

    def __open(self, _path):
        image = PilImage.open(_path)
        if image.mode != 'RGB':  # fixed image mode
            image = image.convert('RGB')
        return image

    def gray(self, dest_path=None):
        try:
            img = PilImage.open(self.src_path).convert('LA')
        except ValueError:
            img = PilImage.open(self.src_path).convert('L')
        if dest_path is not None:
            img.save(dest_path)
        return img

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
        max_offset = self._get_max_crop_size(crop_params.get('max_crop_size', '50%'), height)
        factor = crop_params.get('auto_crop_factor')
        pixels = img.load()
        crop_type = int(pixels[0,0] > 125)

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

    def crop_manual(self, dest_path=None):
        image = self.__open(self.src_path)
        pass

    def crop_auto(self, dest_path=None):
        img = self.gray(self.src_path)
        top_offset = self.__get_blank_size(img)
        img = img.rotate(90)
        right_offset = self.__get_blank_size(img)
        img = img.rotate(90)
        bottom_offset = self.__get_blank_size(img)
        img = img.rotate(90)
        left_offset = self.__get_blank_size(img)
        
        if top_offset or right_offset or bottom_offset or left_offset:
            image = self.__open(self.src_path)
            # image.crop
        pass
