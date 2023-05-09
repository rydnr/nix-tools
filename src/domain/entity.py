import functools
from datetime import datetime
import importlib
import inspect
import re

_primary_key_attributes = {}
_filter_attributes = {}
_attributes = {}

def _add_attribute(self, func):
    key = self.__class__
    if not key in _attributes:
        _attributes[key] = [ ]
    if not func.__name__ in _attributes[key]:
        _attributes[key].append(func.__name__)

def attribute(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        _add_attribute(self, func)
        return func(self, *args, **kwargs)
    return wrapper


def primary_key_attribute(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        key = self.__class__
        if not key in _primary_key_attributes:
            _primary_key_attributes[key] = []
        if not func.__name__ in _primary_key_attributes[key]:
            _primary_key_attributes[key].append(func.__name__)
        _add_attribute(self, func)
        return func(self, *args, **kwargs)
    return wrapper

def filter_attribute(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        key = self.__class__
        if not key in _filter_attributes:
            _filter_attributes[key] = []
        if not func.__name__ in _filter_attributes[key]:
            _filter_attributes[key].append(func.__name__)
        _add_attribute(self, func)
        return func(self, *args, **kwargs)
    return wrapper

class Entity:

    @classmethod
    def primary_key(cls):
        result = []
        key = cls
        if key in _primary_key_attributes:
            result = _primary_key_attributes[key]
        return result


    @classmethod
    def filter_attributes(cls):
        result = []
        key = cls
        if key in _filter_attributes:
            result = _filter_attributes[key]
        return result

    @classmethod
    def attributes(cls):
        result = []
        key = cls
        if key in _attributes:
            result = _attributes[key]
        return [ "id" ] + result + [ "_created", "_updated" ]


    """
    Represents an entity.
    """
    def __init__(self):
        """Creates a new Entity instance"""
        self._id = id(self)
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

    @classmethod
    def _propagate_attributes(cls):
        for cls in _attributes.keys():
            for subclass in cls.__subclasses__():
                if subclass not in _attributes:
                    _attributes[subclass] = _attributes[cls].copy()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._propagate_attributes()

    def __str__(self):
        result = []
        key = self.__class__
        if key in _attributes:
            result.append(f"'id': '{self._id}'")
            result.append(f"'class': '{self.__class__.__name__}'")
            for attr in _attributes[key]:
                result.append(f"'{attr}': '" + str(getattr(self, f"_{attr}")) + "'")
            result.append(f"'_created': '{self._created}'")
            if self._updated:
                result.append(f"'_updated': '{self._updated}'")

        return "{ " + ", ".join(result) + " }"

    def __repr__(self):
        return self.__str__()

    def __setattr__(self, varName, varValue):
        key = self.__class__
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
