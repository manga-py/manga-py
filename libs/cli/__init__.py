from argparse import ArgumentParser


class Cli:

    status = True

    def __init__(self, parser: object, args: ArgumentParser):
        sels.args = args.get_arguments()

    @staticmethod
    def get_arguments() -> ArgumentParser:

        args_parser = ArgumentParser()

        args_parser.add_argument('-u', '--url', type=str, required=False, help='Downloaded url', default='')
        args_parser.add_argument('-n', '--name', type=str, required=False, help='Manga name', default='')
        args_parser.add_argument('-d', '--destination', type=str, required=False,
                           help='Destination folder (Default = current directory', default='')
        args_parser.add_argument('-i', '--info', action='store_const', required=False, const=True, default=False)
        args_parser.add_argument('-p', '--progress', action='store_const', required=False, const=True,
                           help='Show progress bar (don\'t work on Dos)', default=False)
        args_parser.add_argument('-s', '--skip-volumes', type=int, required=False, help='Skip volumes (count)', default=0)
        args_parser.add_argument('-c', '--max-volumes', type=int, required=False,
                           help='Maximum volumes for downloading 0=All (count)', default=0)
        args_parser.add_argument('--user-agent', required=False, type=str, help='Don\'t work from protected sites',
                           default='')
        args_parser.add_argument('--proxy', required=False, type=str, help='Http proxy', default='')

        args_parser.add_argument('--no-name', action='store_const', required=False,
                           help='Don\'t added manga name to the path', const=True, default=False)
        args_parser.add_argument('--allow-webp', action='store_const', required=False, help='Allow downloading webp images',
                           const=True, default=False)
        args_parser.add_argument('--force-png', action='store_const', required=False,
                           help='Force conversation images to png format', const=True, default=False)
        args_parser.add_argument('--reverse-downloading', action='store_const', required=False,
                           help='Reverse volumes downloading', const=True, default=False)
        args_parser.add_argument('--rewrite-exists-archives', action='store_const', required=False, const=True, default=False)
        args_parser.add_argument('--no-multi-threads', action='store_const', required=False,
                           help='Disallow multi-threads images downloading', const=True, default=False)
        args_parser.add_argument('-xt', required=False, type=int, help='Manual image crop with top side', default=0)
        args_parser.add_argument('-xr', required=False, type=int, help='Manual image crop with right side', default=0)
        args_parser.add_argument('-xb', required=False, type=int, help='Manual image crop with bottom side', default=0)
        args_parser.add_argument('-xl', required=False, type=int, help='Manual image crop with left side', default=0)

        args_parser.add_argument('--crop-blank', action='store_const', required=False, help='Crop white lines on image',
                           const=True, default=False)
        args_parser.add_argument('--crop-blank-factor', required=False, type=int, help='Find factor 0..255. Default: 100',
                           default=100)
        args_parser.add_argument('--crop-blank-max-size', required=False, type=int,
                           help='Maximum crop size (px). Default: 30', default=30)
        # args_parser.add_argument()

        args_parser.add_argument('--cli', action='store_const', required=False, const=True, help='Use cli interface',
                                 default=False)

        return args_parser

    @staticmethod
    def input(prompt: str = ''):
        return input(prompt=prompt + '\n')
