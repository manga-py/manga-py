from PIL import Image as PilImage, ImageDraw, ImageChops
import imghdr


class Image:
    _image = None

    def __init__(self, image):
        if isinstance(image, str):
            self._image = PilImage.open(image)
        elif isinstance(image, PilImage.Image):
            self._image = image

    def calc_sides(self, need, inside=True):
        image = self._image.copy()
        orig = image.size
        if inside:
            scale = max(*orig) / max(*need)
        else:
            scale = min(*orig) / min(*need)
        return image.resize((scale * need[0], scale * need[1]), PilImage.ANTIALIAS)

    def __add__(self, other):
        margin = 5
        size = self._image.size
        other_size = other.size
        if size[0] < other_size[0] or size[1] < other_size[1]:
            other_size = (size[0] - margin*2, size[1] - margin*2)
            other.resize(other_size, PilImage.ANTIALIAS)
        x = size[0] - other_size[1]
        self._image.paste(other)

    @staticmethod
    def real_extension(path):
        ext = imghdr.what(path)
        if ext:
            ext = '.' + ext
        return ext

    def auto_crop(self):
        """
        :param dest_path:
        :return:
        """
        bg = PilImage.new(
            self._image.mode,
            self._image.size,
            self._image.getpixel((1, 1))
        )
        diff = ImageChops.difference(self._image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        diff.close()
        if bbox:
            image = self._image.crop(bbox)
        else:
            image = self._image.copy()
        return image
