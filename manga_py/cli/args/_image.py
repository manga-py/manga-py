from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Image options')

    args.add_argument('-E', '--not-change-files-extension', action='store_const',
                      help='Save files "as is"', const=True, default=False)

    args.add_argument('--png', action='store_const', default=False,
                      help='Force conversation images to png format', const=True)
    args.add_argument('--jpg', action='store_const', default=False,
                      help='Force conversation images to jpg format', const=True)

    args.add_argument('-B', '--force-black-white', action='store_const', default=False,
                      help='Force apply black and white image filter', const=True)

    args.add_argument('--Xt', metavar='pix', type=int, help='Manual image crop with top side', default=0)
    args.add_argument('--Xr', metavar='pix', type=int, help='Manual image crop with right side', default=0)
    args.add_argument('--Xb', metavar='pix', type=int, help='Manual image crop with bottom side', default=0)
    args.add_argument('--Xl', metavar='pix', type=int, help='Manual image crop with left side', default=0)

    args.add_argument('--crop-blank', action='store_const', default=False,
                      help='Crop blank borders', const=True)
