#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from manga_py import main
from manga_py.cli.args import get_cli_arguments
import argcomplete


# class aasd:
#     @classmethod
#     def method1(cls):
#         return cls.__name__
#
#     def method2(self):
#         return aasd.__name__
#
#     @staticmethod
#     def method3():
#         return aasd.__name__
#
#     @property
#     def method4(self):
#         return self.__class__.__name__
#
#
# class bbsd(aasd):
#     pass
#
#
# a = aasd()
# b = bbsd()
# print([a.method1(), aasd.method1()])
# print([a.method2(), aasd.method2(aasd())])
# print([a.method3(), aasd.method3()])
# print([a.method4, aasd.method4])
# print()
# print([b.method1(), bbsd.method1()])
# print([b.method2(), bbsd.method2(bbsd())])
# print([b.method3(), bbsd.method3()])
# print([b.method4, bbsd.method4])
# exit()

if __name__ == '__main__':
    argcomplete.autocomplete(get_cli_arguments())
    main()
