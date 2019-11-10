from argparse import ArgumentParser


def _images_options(args_parser: ArgumentParser):  # pragma: no cover
    args = args_parser.add_argument_group('Image options')

    args.add_argument('-E', '--not-change-files-extension', action='store_true',
                      help='Save downloaded files to archive "as is".')
    args.add_argument('--force-jpg', action='store_true',
                      help='Convert `*.webp` images to `*.jpg` format.')


