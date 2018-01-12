#!/usr/bin/env python3
# -- coding: utf8 --
# :author: nvagus
# :time: 12/22/17-3:47 PM
# :package: proto

import inspect


class __Type:
    def method(self):
        pass


_method = type(__Type().method)
_function = type(__Type.method)


class Method(object):
    """ marks if a function is a method
    """

    def __init__(self, func):
        """ marks a function as a method
        :param func: the function to be bound as method, class method, or static method
        """
        self.func = func

    def __call__(self, *args, **kwargs):
        """ a Method can be called as normal function
        """
        return self.func(*args, **kwargs)

    def method(self, instance):
        """ bound the function with an instance
        :param instance: the instance who own the method
        :return: a bound method with the given instance
        """
        return _method(self.func, instance)


class ClassMethod(Method):
    """ marks if a function is a method
    """
    pass


class StaticMethod(Method):
    """ marks if a function is a method
    """
    pass


def __attr__(cls, item, bound=None, skip=False, mo=False):
    """ get an attribute from an instance
    :param cls: the instance
    :param item: the attribute
    :param bound: what instance to be bound, should be initially called with None
    :param skip: whether to skip the instance itself, that only find the attribute in its supers
    :param mo: find method only, which should be an attribute of its class
    :return: the attribute of an item met the given criteria
    """
    if cls is not Proto:
        if not skip and not mo:
            result = cls.__proto__.get(item)
            if result is not None:
                if bound is not None:
                    if isinstance(result, Method):
                        yield result.method(bound)
                    else:
                        yield result if not hasattr(result, '__get__') or isinstance(result, _function) \
                            else result.__get__(bound, bound.__class__)
                else:
                    yield result if not hasattr(result, '__get__') or isinstance(result, _function) \
                            else result.__get__(cls, cls.__class__)
        yield from __attr__(cls.__class__, item, skip=skip, bound=cls)
        for sup in cls.__super__:
            yield from __attr__(sup, item, bound=bound, mo=mo)


class Proto(type):
    """ the origin of every Proto types and instances
    """
    __proto__ = {}

    def __new__(mcs, *args, **kwargs):
        """ initialize a new class that is an instance of this metaclass
        :return: the instance class generated by the metaclass
        """
        name = kwargs.get('__name__') or 'Anonymous Proto'
        sup = tuple(kwargs.get('__super__') or ())
        return super(Proto, mcs).__new__(
            mcs, name, (mcs,), {
                '__proto__': {},
                '__super__': sup,
                '__name__': name
            }
        )

    def __init__(cls, *args, **kwargs):
        """ initialize a Proto instance, if it has a __proto_init__ method, call it
        :param args, kwargs: argument for the init call
        """
        super(Proto, cls).__init__(cls, cls)
        if '__name__' in kwargs:
            kwargs.pop('__name__')
        if '__super__' in kwargs:
            kwargs.pop('__super__')
        if cls.__class__ is not Proto:
            try:
                init = cls.method_only(cls, '__proto_init__')
            except AttributeError:
                return
            init(*args, **kwargs)

    def __setattr__(cls, key, value):
        """ set an attribute for a Proto instance
        :param key: the key of the attribute
        :param value: the new value of the attribute, descriptor supported
        :return: no return
        """
        try:
            cls.__proto__[key].__set__(cls, value)
        except (AttributeError, KeyError):
            cls.__proto__[key] = value

    def __getattr__(cls, item):
        """ get an attribute from a Proto instance
        :param item: the key of the attribute
        :return: the attribute
        """
        try:
            return next(__attr__(cls, item))
        except (StopIteration, RecursionError):
            pass
        raise AttributeError(item)

    @staticmethod
    def super(cls, item):
        """ get an attribute from the supers of a Proto instance
        :param cls: the instance
        :param item: the key of the attribute
        :return: the attribute
        """
        try:
            return next(__attr__(cls, item, skip=True))
        except (StopIteration, RecursionError):
            pass
        raise AttributeError(item)

    @staticmethod
    def method_only(cls, item):
        """ get a method from the class of a Proto instance
        :param cls: the instance
        :param item: the key of the attribute
        :return: the attribute
        """
        try:
            return next(__attr__(cls, item, mo=True))
        except (StopIteration, RecursionError):
            pass
        raise AttributeError(item)

    @staticmethod
    def super_method_only(cls, item):
        """ get a method from the super class of a Proto instance
        :param cls: the instance
        :param item: the key of the attribute
        :return: the attribute
        """
        try:
            return next(__attr__(cls, item, skip=True, mo=True))
        except (StopIteration, RecursionError):
            pass
        raise AttributeError(item)

    @property
    def init(cls):
        """ hook wrapper of __init__
        :return: a wrapper that set the function as proto_init hook
        """

        def __wrapper__(f):
            cls.__proto_init__ = Method(f)

        return __wrapper__

    @property
    def enter(cls):
        """ hook wrapper of __enter__
        :return: a wrapper that set the function as proto_enter hook
        """

        def __wrapper__(f):
            cls.__proto_enter__ = Method(f)

        return __wrapper__

    @property
    def exit(cls):
        """ hook wrapper of __exit__
        :return: a wrapper that set the function as proto_exit hook
        """

        def __wrapper__(f):
            cls.__proto_exit__ = Method(f)

        return __wrapper__

    @property
    def getitem(cls):
        """ hook wrapper of __getitem__
        :return: a wrapper that set the function as proto_getitem hook
        """

        def __wrapper__(f):
            cls.__proto_getitem__ = Method(f)

        return __wrapper__

    @property
    def setitem(cls):
        """ hook wrapper of __setitem__
        :return: a wrapper that set the function as proto_setitem hook
        """

        def __wrapper__(f):
            cls.__proto_setitem__ = Method(f)

        return __wrapper__

    @property
    def method(cls):
        """ wrapper of method
        :return: a wrapper that set the function as a method
        """

        def __wrapper__(f):
            setattr(cls, f.__name__, Method(f))

        return __wrapper__

    @property
    def class_method(cls):
        """ wrapper of class method
        :return: a wrapper that set the function as a class method
        """

        def __wrapper__(f):
            setattr(cls, f.__name__, _method(f, cls))

        return __wrapper__

    @property
    def static_method(cls):
        """ wrapper of static method
        :return: a wrapper that set the function as a static method
        """

        def __wrapper__(f):
            setattr(cls, f.__name__, f)

        return __wrapper__

    def __enter__(cls):
        """ default enter protocol, which set attribute when exit
        :return: the cls itself
        """
        try:
            user_def_enter = cls.method_only(cls, '__proto_enter__')
        except AttributeError:
            cls.__proto_previous_locals__ = inspect.currentframe().f_back.f_locals.copy()
            return cls
        return user_def_enter()

    def __exit__(cls, exc_type, exc_val, exc_tb):
        """ default exit protocol, which set the attributes that newly defined with the block
        :return: None
        """
        try:
            user_def_exit = cls.method_only(cls, '__proto_exit__')
        except AttributeError:
            previous_locals = cls.__proto_previous_locals__
            for key, val in inspect.currentframe().f_back.f_locals.items():
                if key not in previous_locals or previous_locals[key] not in (val, cls):
                    if isinstance(val, _function):
                        setattr(cls, key, Method(val))
                    elif not isinstance(val, Method):
                        setattr(cls, key, val)
                    elif isinstance(val, ClassMethod):
                        setattr(cls, key, val.method(cls))
                    else:
                        setattr(cls, key, val.func)
            return
        user_def_exit(exc_type, exc_val, exc_tb)

    def __getitem__(cls, item):
        """ hook redirect
        """
        return cls.method_only(cls, '__proto_getitem__')(item)

    def __setitem__(cls, key, value):
        """ hook redirect
        """
        return cls.method_only(cls, '__proto_setitem__')(key, value)


def proto(*sup):
    """ create a new proto instance with its supers
    :param sup: the super proto
    :return: a wrapper that make the function as an init method of the new proto
    """

    def __wrapper__(f):
        cls = Proto(__name__=f.__name__, __super__=sup)
        cls.__proto_init__ = Method(f)
        return cls

    return __wrapper__


def combine(*parts, name=None):
    """ combine several proto to be a new proto
    :param parts: the super proto
    :param name: the name of the new proto
    :return: the new proto
    """
    return Proto(__name__=name or f'Combination of {" & ".join(map(lambda x: x.__name__, parts))}', __super__=parts)


def is_instance(cls, target, skip=True):
    """ tell if a proto instance is the instance of another proto instance
    :param cls: the first proto instance
    :param target: the target proto instance
    :param skip: should be True when called, for inner recursion
    :return: whether cls is the target's instance
    """
    if isinstance(target, Proto):
        if not skip and cls is target:
            return True
        else:
            if is_instance(cls.__class__, target, skip=False):
                return True
            for sup in cls.__super__:
                if is_instance(sup, target, skip=skip):
                    return True
    else:
        for tgt in target:
            if is_instance(cls, tgt):
                return True
    return False
