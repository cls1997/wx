# coding: utf8
import copy
import logging
import types

from .fields import Field

logger = logging.getLogger("WechatAPI")


class WechatMessageMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name in ["WechatMessage", ]:
            return type.__new__(mcs, name, bases, attrs)
        data = {}
        tmp_attrs = copy.deepcopy(attrs)
        for base in bases:
            if hasattr(base, '__data__'):
                tmp_attrs.update(copy.deepcopy(base.__data__))
        for k, v in tmp_attrs.items():
            if isinstance(v, Field):
                # logger.debug(
                #     'Found Field {}: {} ==> {}'.format(name, k, v))
                data[k] = v
                if k in attrs:
                    attrs.pop(k)

        logger.debug("Entity %s(%s)'s attributes: %s", name,
                     mcs, [k for k in data.keys()])
        mcs = type.__new__(mcs, name, bases, attrs)
        mcs.__data__ = data
        return mcs


class WechatMessage(dict, metaclass=WechatMessageMetaclass):
    def __init__(self, **args):
        logger.debug("Message initializing .%s %s %s", self.__class__,
                     [v.name for v in self._fields.values()],
                     [v for v in args.values()]
                     )
        # TODO: Encrypt Message Handle
        if len(args) != len(self._fields):
            raise TypeError("{} takes exactly {} argument ({} given)".format(
                self.__class__.__name__, len(self._fields), len(args)))
        for k, v in self._fields.items():
            try:
                self[k] = args[v.name]
            except KeyError:
                raise TypeError(
                    "'{}' has no attribute '{}({})'".format(self.__class__, k, v.name))
        super().__init__(args)

    def __getattr__(self, key):
        if key in self._fields.keys():
            key = self._fields[key].name
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (self.__class__, key))

    def __setattr__(self, key, value):
        # TODO: Type judge
        logger.debug("self data: %s", self._fields)
        if (isinstance(value, types.FunctionType)):
            super().__setattr__(key, types.MethodType(value, self))
            return
        for v in self._fields.values():
            if v.name == key:
                print("QWE")
        self[key] = value

    @property
    def _fields(self):
        return self.__class__.__data__

#
