from PIL import Image as PilImage
from os import path


class Image:
    @staticmethod
    def convert(src_path, dest_path=None, quality=95):
        """
        @ see http://pillow.readthedocs.io/en/3.4.x/handbook/image-file-formats.html
        :param src_path:
        :param dest_path:
        :param quality:
        :return:
        """
        if not path.isfile(src_path):
            return False
        try:
            image = PilImage.open(src_path)
            if image.mode != 'RGB':  # fixed image mode
                image = image.convert('RGB')
            if not dest_path:
                dest_path = '{}.{}'.format(src_path[:src_path.rfind('.')], src_path[src_path.frind('.')])
            image.save(dest_path, quality=quality)
            return dest_path
        except OSError:
            return False

    @staticmethod
    def crop_manual(src_path, dest_path):
        pass

    @staticmethod
    def crop_auto(src_path, dest_path):
        pass
