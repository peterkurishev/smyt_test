# -*- coding: utf-8 -*-
from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from StringIO import StringIO


def yaml_string_to_models(yaml_string):
    stream = StringIO(yaml_string)
    models = load(stream, Loader)

    return models


def yaml_to_models(yaml_file):
    stream = file(yaml_file, 'r')
    models = load(stream, Loader)

    return models