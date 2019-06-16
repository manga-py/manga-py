from sys import stdout
from pprint import pprint


def print_lib(*_args, file=stdout, **kwargs):
    # todo: windows cmd stdout errors
    pprint(*_args, stream=file, **kwargs)
