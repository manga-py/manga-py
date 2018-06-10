try:
    from atexit import register as atexit_register
    from os import makedirs
    from os import path
    from shutil import rmtree
    from sys import argv, exit
    from json import dumps

    from .cli import Cli, get_cli_arguments
    from .fs import get_temp_path
    from .info import Info

except Exception:
    print('Setup in progress?')
    exit()

__author__ = 'Sergey Zharkov'
__license__ = 'MIT'
__email__ = 'sttv-pc@mail.ru'


@atexit_register
def before_shutdown():
    temp_dir = get_temp_path()
    path.isdir(temp_dir) and rmtree(temp_dir)


def main():
    temp_path = get_temp_path()
    path.isdir(temp_path) or makedirs(temp_path)

    args = get_cli_arguments()
    parse_args = args.parse_args()

    # if parse_args.server:
    #     server_mode = Server(args)
    #     exit()

    _info = Info(parse_args)

    try:
        cli_mode = Cli(args)
        cli_mode.start()
        code = 0
    except Exception as e:
        code = 1
        _info.set_error(e, code)

    if parse_args.print_json:
        print(dumps(_info.get()))

    exit(code)


if __name__ == '__main__':
    main()
