from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Image options (Not implemented now)')

    args.add_argument('--png', action='store_true', help='Force conversation images to png format')
    args.add_argument('--jpg', action='store_true', help='Force conversation images to jpg format')

    args.add_argument('-g', '--grayscale', action='store_true', help='Force apply grayscale image filter')

    args.add_argument('--Xt', metavar='px', type=int, help='Manual image crop with top side', default=0)
    args.add_argument('--Xr', metavar='px', type=int, help='Manual image crop with right side', default=0)
    args.add_argument('--Xb', metavar='px', type=int, help='Manual image crop with bottom side', default=0)
    args.add_argument('--Xl', metavar='px', type=int, help='Manual image crop with left side', default=0)

    args.add_argument('-b', '--crop-blank', action='store_true', help='Crop blank borders')

    args.add_argument('--split-images', action='store_true', help='Try to split long images')
