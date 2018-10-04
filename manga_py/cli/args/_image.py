from argparse import ArgumentParser


def main(args_parser: ArgumentParser):
    args = args_parser.add_argument_group('Image options')

    args.add_argument('--png', action='store_const', default=False,
                      help='Force conversation images to png format', const=True)
    args.add_argument('--jpg', action='store_const', default=False,
                      help='Force conversation images to jpg format', const=True)

    args.add_argument('-g', '--grayscale', action='store_const', default=False,
                      help='Force apply grayscale image filter', const=True)

    args.add_argument('--Xt', metavar='px', type=int, help='Manual image crop with top side', default=0)
    args.add_argument('--Xr', metavar='px', type=int, help='Manual image crop with right side', default=0)
    args.add_argument('--Xb', metavar='px', type=int, help='Manual image crop with bottom side', default=0)
    args.add_argument('--Xl', metavar='px', type=int, help='Manual image crop with left side', default=0)

    args.add_argument('-C', '--crop-blank', action='store_const', default=False,
                      help='Crop blank borders', const=True)

    args.add_argument('--split-image', action='store_const', default=False,
                      help='Try to split long images', const=True)
