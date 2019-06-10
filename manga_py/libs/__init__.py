from sys import stdout


def print_lib(*_args, file=stdout):
    # todo: windows cmd stdout errors
    print(*_args, file=file)
