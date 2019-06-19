from sys import stdout
try:  # fixme: debug-only
    from pprint import pprint
except ImportError:
    def pprint(obj, stream=None, indent=1, width=80, depth=None, *args, compact=False):
        print(obj, *args, file=stream)


def print_lib(*_args, file=stdout, **kwargs):
    # todo: windows cmd stdout errors
    pprint(*_args, stream=file, **kwargs)
