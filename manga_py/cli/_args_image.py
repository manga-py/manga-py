
def _args_image(args_parser):  # pragma: no cover
    args = args_parser.add_argument_group('Image options')

    args.add_argument(
        '-E',
        '--not-change-files-extension',
        action='store_true',
        help=(
            'Save downloaded files to archive "as is".'
        )
    )

    args.add_argument(
        '-W',
        '--no-webp',
        action='store_true',
        help=(
            'Convert `*.webp` images to `*.jpg` format.'
        )
    )
