from sys import stdout


def print_lib(*_args, file=stdout, **kwargs):
    # todo: windows cmd stdout errors
    print(*_args, file=file, **kwargs)
