try:
    from .cli import Cli
except ImportError as e:
    print(e)


def main():
    Cli().run()


if __name__ == '__main__':
    main()
