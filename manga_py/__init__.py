try:
    from atexit import register as atexit_register
    from os import makedirs
    from os import path
    from shutil import rmtree
    from sys import argv, exit, exc_info, stderr
    from json import dumps
    import traceback

    from .cli import Cli, check_version
    from .cli.args import get_cli_arguments
    from .fs import get_temp_path, get_info
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
    error_lvl = -2
    if args.parse_args().full_error:
        error_lvl = -10
    try:
        _info.start()
        cli_mode = Cli(args, _info)
        cli_mode.start()
        code = 0
    except Exception as e:
        traceback.print_tb(e.__traceback__, error_lvl, file=stderr)
        code = 1
        _info.set_error(e)
    return code


def _run_util(args) -> tuple:
    parse_args = args.parse_args()

    # if parse_args.server:
    #     server_mode = Server(args)
    #     exit()

    _info = Info(parse_args)

    code = _init_cli(args, _info)

    _info = dumps(_info.get())

    return code, _info


def _update_all(args):
    parse_args = args.parse_args()
    print('Update all', file=stderr)
    multi_info = {}

    dst = parse_args.destination
    json_info = get_info(dst)

    for i in json_info:
        parse_args.manga_name = i['manga_name']
        parse_args.url = i['url']
        code, _info = _run_util(args)
        multi_info[i['directory']] = _info
    parse_args.print_json and print(multi_info)


def main():
    temp_path = get_temp_path()
    path.isdir(temp_path) or makedirs(temp_path)

    args = get_cli_arguments()
    parse_args = args.parse_args()

    code = 0
    if parse_args.update_all:
        _update_all(args)
    else:
        code, _info = _run_util(args)
        parse_args.print_json and print(_info)

    exit(code)


if __name__ == '__main__':
    # version = check_version()  # maybe
    # if version['need_update']:
    #     print('Found new version! %s \nSee here: %s' % (
    #         version['tag'],
    #         version['url']
    #     ), file=stderr)

    main()
