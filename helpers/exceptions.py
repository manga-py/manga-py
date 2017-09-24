#!/usr/bin/python3
# -*- coding: utf-8 -*-


class DirectoryNotWritable(AttributeError):
    pass


class DirectoryNotExists(AttributeError):
    pass


class VolumesNotFound(AttributeError):
    pass


class StatusError(AttributeError):
    pass


class UrlParseError(AttributeError):
    pass
