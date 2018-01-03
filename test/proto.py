#!/usr/bin/env python3
# -- coding: utf8 --
# :author: nvagus
# :time: 12/22/17-3:47 PM
# :package: proto.test

import code

from proto import proto


@proto()
def person(self, name):
    self._name = name


# alice = person('Alice')
#
#
# @alice.hook
# def __new__(self, age):
#     self._age = age
#
#
# little_alice = alice(6)

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

    @staticmethod
    def unbounded_method(f):
        return


code.interact(local=locals())
