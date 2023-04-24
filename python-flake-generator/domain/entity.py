import sys
from pathlib import Path

base_folder = str(Path(__file__).resolve().parent.parent)
if base_folder not in sys.path:
    sys.path.append(base_folder)

import functools
from datetime import datetime
import inspect
import re

_primary_key_attributes = {}
_filter_attributes = {}
_attributes = {}

def attribute(func):
    key = inspect.getmodule(func).__name__
    if not key in _attributes:
        _attributes[key] = [ ]
    _attributes[key].append(func.__name__)
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return wrapper


def primary_key_attribute(func):
    key = inspect.getmodule(func).__name__
    if not key in _primary_key_attributes:
        _primary_key_attributes[key] = []
    _primary_key_attributes[key].append(func.__name__)
    attribute(func)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def filter_attribute(func):
    key = inspect.getmodule(func).__name__
    if not key in _filter_attributes:
        _filter_attributes[key] = []
    _filter_attributes[key].append(func.__name__)
    attribute(func)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class Entity:

    @classmethod
    def primary_key(cls):
        result = []
        key = cls.__module__
        if key in _primary_key_attributes:
            result = _primary_key_attributes[key]
        return result


    @classmethod
    def filter_attributes(cls):
        result = []
        key = cls.__module__
        if key in _filter_attributes:
            result = _filter_attributes[key]
        return result


    @classmethod
    def attributes(cls):
        result = []
        key = cls.__module__
        if key in _attributes:
            result = _attributes[key]
        return [ "id" ] + result + [ "_created", "_updated" ]


    """
    Represents an entity.
    """
    def __init__(self, id):
        """Creates a new Entity instance"""
        self._id = id
        self._created = datetime.now()
        self._updated = None


    @property
    def id(self):
        return self._id


    @property
    def created(self):
        return self._created


    @property
    def updated(self):
        return self._updated


    def __str__(self):
        result = []
        key = inspect.getmodule(self.__class__).__name__
        if key in _attributes:
            result.append(f"'id': '{self._id}'")
            for attr in _attributes[key]:
                result.append(f"'{attr}': '" + str(getattr(self, f"_{attr}")) + "'")
            result.append(f"'_created': '{self._created}'")
            if self._updated:
                result.append(f"'_updated': '{self._updated}'")

        return "{ " + ", ".join(result) + " }"


    def __setattr__(self, varName, varValue):
        key = inspect.getmodule(self.__class__).__name__
        if key in _attributes:
            if varName in [ x for x in _attributes[key] ]:
                self._updated = datetime.now()
        super(Entity, self).__setattr__(varName, varValue)

    def __eq__(self, other):
        result = False
        if isinstance(other, self.__class__):
            result = True
            for key in self.__class__.primary_key():
                if getattr(self, key, None) != getattr(other, key, None):
                    result = False
                    break
        return result

    def __hash__(self):
        attrs = []
        for key in self.__class__.primary_key():
            attrs.append(getattr(self, key, None))

        return hash(tuple(attrs))
