try:
    from atexit import register as atexit_register
    from os import makedirs
    from os import path
    from shutil import rmtree
    from sys import argv, exit, exc_info, stderr
    from json import dumps
    import traceback

    from .meta import __version__

except Exception as e:
    print(e)
    print('Setup in progress?', file=stderr)
    print('manga-py version: %s' % __version__, file=stderr)
    exit()


def main():
    exit()


if __name__ == '__main__':
    main()
