import unittest
from os import path

from PIL import Image as PilImage

from manga_py import fs
from manga_py.image import Image

root_path = path.dirname(path.realpath(__file__))

files_paths = [
    ['/files/img1.jpg', '/temp/img1.jpg'],
    ['/files/img2.png', '/temp/img2.png'],
    ['/files/img3.jpg', '/temp/img3.jpg'],
    ['/files/img4.jpg', '/temp/img4.jpg'],
    ['/files/img5.png', '/temp/img5.png'],
    ['/files/img6.gif', '/temp/img6.gif'],
    ['/files/img7.webp', '/temp/img7.webp'],
]


class TestImages(unittest.TestCase):

    def test_manual_crop(self):
        for file in files_paths:
            fs.unlink(root_path + file[1])

            image = PilImage.open(root_path + file[0])
            sizes = image.size
            image.close()

            img = Image(root_path + file[0])
            img.crop_manual((10, 0, image.size[0], image.size[1]), root_path + file[1])
            img.close()

            cropped_image = PilImage.open(root_path + file[1])
            cropped_sizes = cropped_image.size
            cropped_image.close()

            self.assertTrue((sizes[0] - cropped_sizes[0]) == 10)

    def test_manual_crop_with_offsets(self):
        for file in files_paths:
            fs.unlink(root_path + file[1])

            image = PilImage.open(root_path + file[0])
            sizes = image.size
            image.close()

            img = Image(root_path + file[0])
            img.crop_manual_with_offsets((10, 0, 0, 0), root_path + file[1])
            img.close()

            cropped_image = PilImage.open(root_path + file[1])
            cropped_sizes = cropped_image.size
            cropped_image.close()

            self.assertTrue((sizes[0] - cropped_sizes[0]) == 10)

    def test_auto_crop1(self):
        file = files_paths[0]
        fs.unlink(root_path + file[1])

        image = PilImage.open(root_path + file[0])
        sizes = image.size
        image.close()

        img = Image(root_path + file[0])
        img.crop_auto(root_path + file[1])
        img.close()

        cropped_image = PilImage.open(root_path + file[1])
        cropped_sizes = cropped_image.size
        cropped_image.close()

        self.assertTrue(sizes[0] > cropped_sizes[0])

    def test_auto_crop2(self):
        file = files_paths[1]
        fs.unlink(root_path + file[1])

        image = PilImage.open(root_path + file[0])
        sizes = image.size
        image.close()

        img = Image(root_path + file[0])
        img.crop_auto(root_path + file[1])
        img.close()

        cropped_image = PilImage.open(root_path + file[1])
        cropped_sizes = cropped_image.size
        cropped_image.close()

        self.assertTrue(sizes[0] == cropped_sizes[0])

    def test_auto_crop3(self):
        file = files_paths[4]
        fs.unlink(root_path + file[1])

        image = PilImage.open(root_path + file[0])
        sizes = image.size
        image.close()

        img = Image(root_path + file[0])
        img.crop_auto(root_path + file[1])
        img.close()

        cropped_image = PilImage.open(root_path + file[1])
        cropped_sizes = cropped_image.size
        cropped_image.close()

        self.assertTrue(sizes[0] == (2 + cropped_sizes[0]))  # 2px black line

    def test_image_not_found(self):
        self.assertRaises(AttributeError, lambda: Image(root_path))

    def test_gray1(self):
        file = files_paths[1]
        fs.unlink(root_path + file[1])

        image = Image(root_path + file[0])
        image.gray(root_path + file[1])
        image.close()

        image = PilImage.open(root_path + file[1])
        index = image.mode.find('L')
        image.close()

        self.assertTrue(index == 0)

    def test_convert(self):
        file = files_paths[0][0]
        image = Image(root_path + file)

        basename = file[0:file.find('.')]
        basename = root_path + '/temp' + basename + '.bmp'
        image.convert(basename)
        image.close()

        self.assertTrue(path.isfile(basename))
