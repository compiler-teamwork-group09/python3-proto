#!/usr/bin/env python3
# -- coding: utf8 --
# :author: nvagus
# :time: 12/22/17-3:47 PM
# :package: proto


class Type:
    def method(self):
        pass


instance = Type()
method = type(instance.method)
unbounded = type(Type.method)


class Method(object):
    def __init__(self, func: unbounded):
        self.__call__ = func

    def __call__(self, *args, **kwargs):
        return self.__call__(*args, **kwargs)

    def __bound__(self, obj):
        if not isinstance(self.__call__, method):
            self.__call__ = method(self.__call__, obj)
        return self

    @staticmethod
    def unbounded_method(f):
        return Method(f)

    @staticmethod
    def bounded_method(obj):
        def __method__(f):
            return Method(f).__bound__(obj)

        return __method__


class Proto(type):
    def __new__(mcs, *args, **kwargs):
        def __attr__(cls, item):
            result = cls.__proto__.get(item)
            if result is not None:
                yield result
            for __super__ in cls.__super__:
                yield from __super__.__attr__(item)

        obj = super(Proto, mcs).__new__(
            mcs, kwargs.pop('__name__'), (mcs,),
            {
                '__proto__': {},
                '__super__': [mcs],
                '__attr__': Method(__attr__)
            }
        )
        obj.__attr__.__bound__(obj)
        return obj

    def __init__(cls, *args, **kwargs):
        # pseudo super call
        super(Proto, cls).__init__(cls, None)
        # cls.__init_proto__(*args, **kwargs)

    @classmethod
    def __attr__(mcs, _):
        # the root class has no attribute: yield from nothing
        yield from ()

    def __setattr__(cls, key, value):
        print(key, value)
        cls.__proto__[key] = value

    def __getattr__(cls, item):
        print(item)
        try:
            return next(cls.__attr__(item))
        except StopIteration:
            pass
        raise AttributeError(item)


def proto(base=Proto):
    def __proto__(f):
        obj = base(__name__=f.__name__)
        return obj

    return __proto__
