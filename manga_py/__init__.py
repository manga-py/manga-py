try:
    from atexit import register as atexit_register
    from os import makedirs
    from os import path
    from shutil import rmtree
    from sys import argv, exit

    from manga_py.cli import Cli, get_cli_arguments
    from manga_py.fs import get_temp_path

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
        #     exit(1 if server_mode.status else 0)

        cli_mode = Cli(args)
        cli_mode.start()
        exit(1 if cli_mode.status else 0)

except Exception:
    def main():
        print('Setup progress?')
