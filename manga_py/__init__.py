try:
    from atexit import register as atexit_register
    from os import makedirs
    from os import path
    from shutil import rmtree
    from sys import argv, exit, exc_info, stderr
    from json import dumps
    import traceback

    from .cli import Cli, get_cli_arguments
    from .fs import get_temp_path
    from .info import Info

except Exception as e:
    print(e)
    print('Setup in progress?')
    exit()

__author__ = 'Sergey Zharkov'
__license__ = 'MIT'
__email__ = 'sttv-pc@mail.ru'


@atexit_register
def before_shutdown():
    temp_dir = get_temp_path()
    path.isdir(temp_dir) and rmtree(temp_dir)


def _init_cli(args, _info):
    try:
        cli_mode = Cli(args, _info)
        cli_mode.start()
        code = 0
    except Exception as e:
        traceback.print_tb(e.__traceback__, -2, file=stderr)
        code = 1
        _info.set_error(e)
    return code


def main():
    temp_path = get_temp_path()
    path.isdir(temp_path) or makedirs(temp_path)

    args = get_cli_arguments()
    parse_args = args.parse_args()

    # if parse_args.server:
    #     server_mode = Server(args)
    #     exit()

    _info = Info(parse_args)

    code = _init_cli(args, _info)

    if parse_args.print_json:
        print(dumps(_info.get()))

    exit(code)


if __name__ == '__main__':
    main()
