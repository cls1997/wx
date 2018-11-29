# coding: utf8
import inspect
import logging
import types

from wechat.messages.fields import Field

logger = logging.getLogger("WechatAPI")


def _is_field(obj): return isinstance(obj, Field)


class WechatMessageMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name in ['WechatMessage', ] or name.startswith('Base'):
            return type.__new__(mcs, name, bases, attrs)

        found_fields = []
        mcs = type.__new__(mcs, name, bases, attrs)
        mcs._fields = {}
        for k, v in inspect.getmembers(mcs, _is_field):
            # logger.debug('Found Field {}: {} ==> {}'.format(name, k, v))
            v.add_to_class(mcs, k)
            found_fields.append(k)

        logger.debug("Entity %s(%s)'s attributes: %s", name,
                     mcs, [k for k in found_fields])
        return mcs


class WechatMessage(metaclass=WechatMessageMetaclass):
    def __init__(self, **args):
        self._data = {}
        logger.debug("Message initializing .%s %s %s", self.__class__,
                     [v.name for v in self._fields.values()],
                     [v for v in args.values()]
                     )
        # TODO: Encrypt Message Handle
        if len(args) != len(self._fields) and False:
            raise TypeError("{} takes exactly {} argument ({} given)".format(
                self.__class__.__name__, len(self._fields), len(args)))
        for k, v in self._fields.items():
            try:
                setattr(self, k, args[v.name])
            except KeyError:
                raise TypeError(
                    "'{}' has no attribute '{}({})'".format(self.__class__, k, v.name))

    # def __getattr__(self, key):
    #     if key in self._fields.keys():
    #         key = self._fields[key].name
    #     try:
    #         return self[key]
    #     except KeyError:
    #         raise AttributeError(
    #             "'%s' object has no attribute '%s'" % (self.__class__, key))
    #
    def __setattr__(self, key, value):
        if isinstance(value, types.FunctionType):
            super().__setattr__(key, types.MethodType(value, self))
            return
        super.__setattr__(key, value)

#
