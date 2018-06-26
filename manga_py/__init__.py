try:
    from atexit import register as atexit_register
    from os import makedirs
    from os import path
    from shutil import rmtree
    from sys import argv, exit, exc_info, stderr
    from json import dumps
    import traceback

except ImportError as e:
    print(e)


def main():
    exit()


if __name__ == '__main__':
    main()
